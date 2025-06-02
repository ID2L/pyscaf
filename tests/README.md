# Suite de tests pour pyscaf

Ce dossier contient l'ensemble des tests automatisés pour le projet `pyscaf`. Les tests couvrent le fonctionnement du CLI, l'interactivité, la génération de structure de projet, et la robustesse face aux entrées utilisateur.

## Organisation des tests

- **test_cli_interactive.py** :
  - Couvre tous les cas d'utilisation du CLI (commandes, options dynamiques, erreurs).
  - Teste l'interactivité (mockée) pour simuler les réponses utilisateur aux questions.
  - Vérifie la structure de projet générée selon les options/actions activées.
  - Teste la robustesse face aux entrées invalides.

## Outils utilisés

- **pytest** : Framework principal pour l'exécution des tests.
- **click.testing.CliRunner** : Pour simuler l'exécution du CLI et capturer les sorties.
- **unittest.mock** : Pour mocker les fonctions interactives (`questionary`) et simuler les réponses utilisateur.

## Lancer les tests

### Avec pytest directement
```bash
pytest
```
Ou pour un fichier précis :
```bash
pytest tests/test_cli_interactive.py
```

### Avec poetry
```bash
poetry run pytest
```
Ou pour un fichier précis :
```bash
poetry run pytest tests/test_cli_interactive.py
```

## Ajouter de nouveaux tests

- Créez un nouveau fichier `test_*.py` ou ajoutez une fonction commençant par `test_` dans un fichier existant.
- Utilisez les fixtures `tmp_path` ou `CliRunner` pour isoler les tests et éviter les effets de bord.
- Pour tester l'interactivité, mockez les appels à `questionary` avec `unittest.mock.patch` et retournez un objet avec une méthode `.ask()`.
- Vérifiez toujours la structure générée sur le disque (fichiers, dossiers) et la sortie du CLI.

## Bonnes pratiques

- Un test = un comportement précis (nom explicite, docstring en anglais, commentaires en français si besoin)
- Nettoyez toujours les fichiers/dossiers temporaires créés
- Privilégiez la robustesse : testez les cas d'erreur et les entrées inattendues
