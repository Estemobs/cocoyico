# Contribution

Merci de vouloir contribuer à Cocoyico !

## Développement

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python cocoyico.py
```

## Vérifications avant PR

```bash
pytest -q
python -m compileall -q .
```

## Pull requests

1. Décrivez le problème résolu et testez le bot dans un serveur de test Discord.
2. Gardez la PR petite et ciblée.
3. Référencez l'issue concernée dans la description.

## Licence

Ce projet est sous licence MIT.
