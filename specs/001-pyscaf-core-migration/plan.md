# Implementation Plan: Migration vers pyscaf-core

**Branch**: `001-pyscaf-core-migration` | **Date**: 2026-04-12 | **Spec**: [spec.md](./spec.md)

## Summary

Transformer `open-pyscaf` d'un monolithe auto-contenu en une application légère qui délègue toute la logique framework à `pyscaf-core`, en suivant exactement le pattern établi par `apps/pyscaf` dans le workspace pyscaf-core.

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: pyscaf-core >= 0.2.1, tomli, tomli-w
**Build System**: Hatchling
**Testing**: pytest + pyscaf_core.testing (plugin pytest)
**Target Platform**: PyPI (package `open-pyscaf`)

## Architecture Decision

Le refactoring suit le pattern **thin app** établi dans `pyscaf-core/apps/pyscaf/`:

1. **`main.py`** — Point d'entrée CLI via `build_cli()` + `make_main()` (≈15 lignes)
2. **`actions/__init__.py`** — Fonction `discover_actions()` via `discover_actions_from_package()` (≈10 lignes)
3. **`actions/*/`** — Actions concrètes inchangées, seuls les imports changent
4. **`testing.py`** — Config pour les tests YAML (≈12 lignes)
5. **Entry-points** — Déclaration des plugins et des tests YAML dans `pyproject.toml`

## Mapping des changements

| Fichier actuel | Action | Remplacé par |
|---|---|---|
| `src/pyscaf/cli.py` | **Réécrire** | `src/pyscaf/main.py` (thin wrapper via `build_cli`) |
| `src/pyscaf/actions/__init__.py` | **Réécrire** | Wrapper autour de `discover_actions_from_package` |
| `src/pyscaf/actions/manager.py` | **Supprimer** | `pyscaf_core.actions.manager.ActionManager` |
| `src/pyscaf/actions/cli_option_to_key.py` | **Supprimer** | `pyscaf_core.actions.cli_option_to_key` |
| `src/pyscaf/preference_chain/` (6 fichiers) | **Supprimer** | `pyscaf_core.preference_chain` |
| `src/pyscaf/tools/` (2 fichiers) | **Supprimer** | `pyscaf_core.tools` |
| `src/pyscaf/actions/core/__init__.py` | **Modifier imports** | `from pyscaf_core import Action, CLIOption` |
| `src/pyscaf/actions/git/__init__.py` | **Modifier imports** | idem |
| `src/pyscaf/actions/jupyter/__init__.py` | **Modifier imports** | idem |
| `src/pyscaf/actions/jupyter_tools/__init__.py` | **Modifier imports** | idem |
| `src/pyscaf/actions/documentation/__init__.py` | **Modifier imports** | idem |
| `src/pyscaf/actions/license/__init__.py` | **Modifier imports** | idem |
| `src/pyscaf/actions/semantic-release/__init__.py` | **Modifier imports** | idem |
| `src/pyscaf/actions/test/__init__.py` | **Modifier imports** | idem |
| — | **Créer** | `src/pyscaf/testing.py` |
| — | **Créer** | `src/pyscaf/action_test_yamls/` (déplacer les YAML de tests) |

## Project Structure (après migration)

```
src/pyscaf/
├── __init__.py              # __version__ uniquement
├── main.py                  # CLI entry point (build_cli + make_main)
├── testing.py               # ActionTestConfig pour les tests YAML
├── actions/
│   ├── __init__.py          # discover_actions() via discover_actions_from_package
│   ├── core/
│   │   ├── __init__.py      # CoreAction (import from pyscaf_core)
│   │   ├── README.md
│   │   ├── config.toml
│   │   ├── default_settings.json
│   │   └── templates/
│   ├── git/
│   │   ├── __init__.py      # GitAction
│   │   └── template.gitignore
│   ├── jupyter/
│   │   ├── __init__.py      # JupyterAction
│   │   ├── config.toml
│   │   └── template.gitignore
│   ├── jupyter_tools/
│   │   ├── __init__.py      # JupyterToolsAction
│   │   ├── config.toml
│   │   └── scripts/
│   ├── documentation/
│   │   ├── __init__.py      # DocumentationAction
│   │   ├── config.toml
│   │   └── scripts/
│   ├── license/
│   │   ├── __init__.py      # LicenseAction
│   │   └── template_*.txt
│   ├── semantic_release/     # Renommé de semantic-release → semantic_release
│   │   ├── __init__.py      # SemanticReleaseAction
│   │   ├── config.toml
│   │   └── github/
│   └── test/
│       ├── __init__.py      # TestAction
│       ├── config.toml
│       └── template_*.py
├── action_test_yamls/       # YAMLs de test déplacés depuis tests/actions/
│   ├── core/
│   ├── git/
│   ├── jupyter/
│   ├── jupyter_tools/
│   ├── documentation/
│   ├── license/
│   ├── semantic_release/
│   └── test/
tests/
├── test_pyscaf_smoke.py     # Smoke tests (discover, CLI help)
└── test_yaml_actions.py     # Tests YAML via create_yaml_tests
```

## Fichiers supprimés

```
src/pyscaf/cli.py                                    # Remplacé par main.py
src/pyscaf/actions/manager.py                        # Dans pyscaf_core
src/pyscaf/actions/cli_option_to_key.py              # Dans pyscaf_core
src/pyscaf/preference_chain/__init__.py              # Dans pyscaf_core
src/pyscaf/preference_chain/__main__.py              # Dans pyscaf_core
src/pyscaf/preference_chain/model.py                 # Dans pyscaf_core
src/pyscaf/preference_chain/chain.py                 # Dans pyscaf_core
src/pyscaf/preference_chain/dependency_loader.py     # Dans pyscaf_core
src/pyscaf/preference_chain/tree_walker.py           # Dans pyscaf_core
src/pyscaf/preference_chain/circular_dependency_error.py  # Dans pyscaf_core
src/pyscaf/preference_chain/dependencies.yaml        # Dans pyscaf_core
src/pyscaf/tools/toml_merge.py                       # Dans pyscaf_core
src/pyscaf/tools/format_toml.py                      # Dans pyscaf_core
tests/actions/conftest.py                            # Remplacé par pyscaf_core.testing
tests/actions/test_actions.py                        # Remplacé par test_yaml_actions.py
tests/preference_chain/                              # Tests du framework → dans pyscaf_core
tests/tools/                                         # Tests du framework → dans pyscaf_core
```

## Implementation Strategy

### Phase 1: Setup — pyproject.toml et structure

Mise à jour de `pyproject.toml` : dépendance pyscaf-core, entry-points, suppression des dépendances devenues transitives.

### Phase 2: Core — Réécriture du module principal

1. Réécrire `actions/__init__.py` avec `discover_actions_from_package`
2. Réécrire le CLI dans `main.py` avec `build_cli` + `make_main`
3. Créer `testing.py`
4. Mettre à jour les imports de chaque action concrète

### Phase 3: Nettoyage — Suppression du code framework

Supprimer `preference_chain/`, `tools/`, `manager.py`, `cli_option_to_key.py`, ancien `cli.py`.

### Phase 4: Tests — Adaptation au framework de test pyscaf-core

1. Déplacer les YAML dans `src/pyscaf/action_test_yamls/`
2. Créer `test_yaml_actions.py` et `test_pyscaf_smoke.py`
3. Supprimer les anciens tests framework

## Dependencies

- `pyscaf-core >= 0.2.1`
- `tomli >= 2.0.0` (utilisé directement par CoreAction)
- `tomli-w >= 1.0.0` (utilisé directement par CoreAction)
