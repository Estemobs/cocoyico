# Cocoyico

Cocoyico est un bot Discord personnalisé qui permet d'enregistrer et gérer des notes (appelées "tags" dans le bot).

## Fonctionnalités principales

- Ajout, suppression, édition et renommage de notes/tags
- Affichage du contenu d'une note/tag spécifique
- Liste complète des notes/tags disponibles
- Affichage de la liste des serveurs où le bot est présent
- Commande personnalisée d'aide intégrée

## Utilisation

### Installation

Installez les dépendances nécessaires :
pip install -r requirements.txt


### Configuration

1. Créez un fichier `secrets.json` à la racine du projet avec le format suivant :
```json 
{ "cocoyico_token": "Votre_Token_Ici" }
```

### Lancement

python cocoyico.py

## Commandes disponibles

- `;addtag [titre]`: Ajoute une nouvelle note/tag
- `;removetag [titre]`: Supprime une note/tag existante
- `;tagedit [titre]`: Modifie le contenu d'une note/tag existante
- `;tagrename [ancien_titre] [nouveau_titre]`: Renomme une note/tag existante
- `;tag [titre]`: Affiche le contenu d'une note/tag spécifique
- `;taglist`: Affiche la liste complète des notes/tags
- `;server_list`: Affiche la liste des serveurs où le bot est présent
- `;help`: Affiche les commandes disponibles avec leurs descriptions

