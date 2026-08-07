import discord
import os
import json
import threading
from discord.ext import commands

# Import all intents from Discord API
intents = discord.Intents.all()

# Create a bot with command prefix ";" and all imported intents
bot = commands.Bot(command_prefix=";", intents=intents)


# Get the absolute path of tags.json
tags_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tags.json')

# Lock for file operations (read/write)
tags_lock = threading.Lock()

# Load the tags from the JSON file, creating it on first run
def load_tags():
    """Load tags from file, return dict."""
    if not os.path.exists(tags_path):
        return {}
    try:
        with open(tags_path, 'r') as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            else:
                return {}
    except (json.JSONDecodeError, OSError):
        # If file is corrupted or unreadable, start with empty dict
        return {}

# Initialize tags
tags = load_tags()

@bot.event
async def on_ready():
    print("bot ready")
    # Changes the bot's playing status to ";help"
    await bot.change_presence(activity=discord.Game(name=";help"))

# Command to add a new tag
@bot.command()
async def addtag(ctx, title: str):
    global tags
    response = "Enter the content for the tag: "
    await ctx.send(response)

    # Check function that returns true if the bot receives a message from the same author and channel as the command
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    # Waits for a message to receive the content of the tag (with timeout)
    try:
        content = await bot.wait_for('message', check=check, timeout=60)
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond. Tag creation cancelled.")
        return

    # Adds the title and content to the tags dictionary
    tags[title] = content.content
    await ctx.send('Tag created.')
    # Write the tags to the JSON file
    with tags_lock:
        with open(tags_path, 'w') as f:
            json.dump(tags, f)

# Command to remove a tag
@bot.command()
async def removetag(ctx, title: str):
    global tags
    if title in tags:
        #if the tag exists
        del tags[title] #remove the tag from the tags dictionary
        with tags_lock:
            with open(tags_path, 'w') as f:
                json.dump(tags, f) #write the tags to the JSON file without the deleted tag
        await ctx.send("Tag removed.") #confirm that the tag has been removed
    else:
        await ctx.send("Tag not found.") #if the tag does not exist, return an error message

# Command to edit a tag
@bot.command()
async def tagedit(ctx, title: str):
    global tags
    if title in tags:
        response = "Enter the new content for the tag: "
        await ctx.send(response)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            content = await bot.wait_for('message', check=check, timeout=60)
        except asyncio.TimeoutError:
            await ctx.send("You timed out. Tag edit cancelled.")
            return

        tags[title] = content.content
        with tags_lock:
            with open(tags_path, 'w') as f:
                json.dump(tags, f) #write the tags to the JSON file with the edited tag
        await ctx.send("Tag edited.")
    else:
        await ctx.send("Tag not found.")

# Command to rename a tag
@bot.command()
async def tagrename(ctx, old_title: str, new_title: str):
    global tags
    if old_title in tags:  # check if tag "old_title" exists
        tags[new_title] = tags[old_title]   # rename tag "old_title" to "new_title"
        del tags[old_title]    # delete the original tag "old_title"
        with tags_lock:
            with open(tags_path, 'w') as f:    # overwrite the tags.json file with the renamed tag
                json.dump(tags, f)
        await ctx.send("Tag renamed.")  # package the operation and send a message that the tag has been renamed
    else:
        await ctx.send("Tag not found.")  # if the original tag "old_title" is not found, send an error message

# Command to display content of a tag given title
@bot.command()
async def tag(ctx, title: str):
    with tags_lock:
        with open(tags_path, 'r') as f:
            tags = json.load(f)
    if title in tags:
        await ctx.send(tags[title])
    else:
        await ctx.send(f"No tag found with the title '{title}'")

@bot.command()
async def taglist(ctx):
    with tags_lock:
        with open(tags_path, 'r') as f:
            tags = json.load(f)
            if tags is None:
                tags = {}

    tag_names = list(tags.keys())
    if not tag_names:
        await ctx.send("No tags available.")
        return
    description = "\n".join(tag_names)
    embed = discord.Embed(title="Tag List", description=description, color=discord.Color.green())
    embed.set_thumbnail(url="https://i.imgur.com/zV874EI.png")
    await ctx.send(embed=embed)


@bot.command()
async def server_list(ctx):
    guilds = bot.guilds
    if not guilds:
        await ctx.send("The bot is not in any server.")
        return
    names = "\n".join(guild.name for guild in guilds)
    embed = discord.Embed(title="Servers", description=names, color=discord.Color.blue())
    await ctx.send(embed=embed)

# Remove the built-in help command
bot.remove_command("help")
# Custom help command to display all available commands and their descriptions
@bot.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(title="Commands", color=discord.Color.green())
    embed.set_thumbnail(url="https://i.imgur.com/zV874EI.png")
    embed.add_field(name="addtag", value="Ajouter un nouvel tag avec le titre et le contenu donné.", inline=False)
    embed.add_field(name="removetag", value="Supprime un tag existant en utilisant son titre.",inline=False)
    embed.add_field(name="tagedit", value="Modifie le contenu d'un tag existant en utilisant son titre", inline=False)
    embed.add_field(name="tagrename", value="Modifie le nom du tag", inline=False)
    embed.add_field(name="tag", value="Affiche le contenu d'un tag avec un titre donné.", inline=False)
    embed.add_field(name="taglist", value="Affiche tous les tags dans une liste organisée.", inline=False)
    embed.add_field(name="server_list", value="Voir la liste des serveurs sur lequel est le bot", inline=False)
    await ctx.send(embed=embed)

# Load secrets
secrets_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'secrets.json')
try:
    with open(secrets_path, "r") as file:
        secrets = json.load(file)
    cocoyico_token = secrets["cocoyico_token"]
except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
    print(f"Error loading secrets: {e}")
    exit(1)

bot.run(cocoyico_token)
