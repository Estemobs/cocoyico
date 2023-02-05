import discord
import os
from discord.ext import commands

# Import all intents from Discord API
intents = discord.Intents.all()

# Create a bot with command prefix ";" and all imported intents
bot = commands.Bot(command_prefix=";", intents=intents)

# Dictionary to store all tags
tags = {}

@bot.event
async def on_ready():
    # Creates an empty tag.txt file when the bot starts
    with open("tags.txt","w") as file:
        file.write("")
    # Prints the location of the tags.txt file in the console log
    print(f"tags.txt created at {os.path.abspath('tags.txt')}")
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

    # Waits for a message to receive the content of the tag
    content = await bot.wait_for('message', check=check)
    # Adds the title and content to the tags dictionary
    tags[title] = content.content
    await ctx.send('Tag created.')
    # Writes the title and content to tags.txt file
    with open("tags.txt", "a") as file:
        file.write(f'{title}: {content.content}\n')
#command to remove a tag
@bot.command()
async def removetag(ctx, title: str):
    global tags
    if title in tags:
        #if the tag exists
        del tags[title] #remove the tag from the tags dictionary
        with open("tags.txt", "w") as file:
            for t,c in tags.items():
                file.write(f'{t}: {c}\n') #rewrite the tags to the tags.txt file without the deleted tag
        await ctx.send("Tag removed.") #confirm that the tag has been removed
    else:
        await ctx.send("Tag not found.") #if the tag does not exist, return an error message

# Command to display content of a tag given title
@bot.command()
async def tag(ctx, title: str):
    global tags
    # If title exists in dictionary tags then display it
    if title in tags:
        await ctx.send(tags[title])
    else:
        await ctx.send("Tag not found.")
# Command to list all tags
@bot.command(pass_context=True)
async def taglist(ctx):
    description = ""
    for title, content in tags.items():
        description += f"**{title}**: {content}\n" 
    embed = discord.Embed(title="Tag List", description=description, color=discord.Color.green())
    embed.set_thumbnail(url="https://i.imgur.com/zV874EI.png")
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
    embed.add_field(name="tag", value="Affiche le contenu d'un tag avec un titre donné.", inline=False)
    embed.add_field(name="taglist", value="Affiche tous les tags dans une liste organisée.", inline=False)
    await ctx.send(embed=embed)
    
    bot.run('token')
