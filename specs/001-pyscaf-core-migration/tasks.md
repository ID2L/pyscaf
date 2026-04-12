# Tasks: Migration vers pyscaf-core

## Phase 1: Setup (pyproject.toml & structure)

**Purpose**: Mettre à jour la configuration du package et préparer la structure.

- [ ] T001 Mettre à jour pyproject.toml : ajouter pyscaf-core en dépendance, entry-points plugins et test_yamls, supprimer les dépendances devenues transitives (click, rich, questionary, pydantic, tomlkit), mettre à jour le script entry-point vers pyscaf.main:main
- [ ] T002 Renommer le dossier src/pyscaf/actions/semantic-release/ en src/pyscaf/actions/semantic_release/ (tiret → underscore pour conformité Python)

## Phase 2: Core — Réécriture des modules principaux

**Purpose**: Remplacer le code framework par les imports pyscaf-core.

- [ ] T003 Réécrire src/pyscaf/actions/__init__.py : remplacer le contenu par un wrapper discover_actions() utilisant discover_actions_from_package de pyscaf_core
- [ ] T004 Créer src/pyscaf/main.py : CLI entry point utilisant build_cli() et make_main() de pyscaf_core
- [ ] T005 Créer src/pyscaf/testing.py : ActionTestConfig pour les tests YAML
- [ ] T006 [P] Modifier src/pyscaf/actions/core/__init__.py : remplacer `from pyscaf.actions import Action, CLIOption` par `from pyscaf_core import Action, CLIOption` et remplacer console.print par logging
- [ ] T007 [P] Modifier src/pyscaf/actions/git/__init__.py : même pattern d'import pyscaf_core
- [ ] T008 [P] Modifier src/pyscaf/actions/jupyter/__init__.py : même pattern d'import pyscaf_core
- [ ] T009 [P] Modifier src/pyscaf/actions/jupyter_tools/__init__.py : même pattern d'import pyscaf_core
- [ ] T010 [P] Modifier src/pyscaf/actions/documentation/__init__.py : même pattern d'import pyscaf_core
- [ ] T011 [P] Modifier src/pyscaf/actions/license/__init__.py : même pattern d'import pyscaf_core
- [ ] T012 [P] Modifier src/pyscaf/actions/semantic_release/__init__.py : même pattern d'import pyscaf_core (attention au renommage du dossier)
- [ ] T013 [P] Modifier src/pyscaf/actions/test/__init__.py : même pattern d'import pyscaf_core

**Checkpoint**: Tous les modules sources importent depuis pyscaf_core

## Phase 3: Nettoyage — Suppression du code framework

**Purpose**: Supprimer tout le code désormais fourni par pyscaf-core.

- [ ] T014 Supprimer src/pyscaf/cli.py
- [ ] T015 Supprimer src/pyscaf/actions/manager.py
- [ ] T016 Supprimer src/pyscaf/actions/cli_option_to_key.py
- [ ] T017 Supprimer src/pyscaf/preference_chain/ (tout le dossier : __init__.py, __main__.py, model.py, chain.py, dependency_loader.py, tree_walker.py, circular_dependency_error.py, dependencies.yaml)
- [ ] T018 Supprimer src/pyscaf/tools/ (tout le dossier : toml_merge.py, format_toml.py)

**Checkpoint**: Aucun code framework ne reste dans src/pyscaf/

## Phase 4: Tests — Migration vers pyscaf_core.testing

**Purpose**: Adapter les tests au framework de test de pyscaf-core.

- [ ] T019 Déplacer les fichiers YAML de tests/actions/{action_name}/*.yaml vers src/pyscaf/action_test_yamls/{action_name}/*.yaml
- [ ] T020 Créer tests/test_yaml_actions.py utilisant create_yaml_tests(entry_point_name="pyscaf")
- [ ] T021 Créer tests/test_pyscaf_smoke.py : test discover_actions (count=8, all subclass Action), test CLI help
- [ ] T022 Supprimer tests/actions/ (conftest.py, test_actions.py, README.md et les YAML déjà déplacés)
- [ ] T023 Supprimer tests/preference_chain/ (tout le dossier)
- [ ] T024 Supprimer tests/tools/ (tout le dossier)
- [ ] T025 Mettre à jour pyproject.toml [tool.pytest.ini_options] : adapter testpaths, retirer --cov=pyscaf pour le remplacer par le bon scope

**Checkpoint**: `pytest tests/` passe sans erreur

## Phase 5: Polish & Validation

- [ ] T026 [P] Lancer ruff check sur src/pyscaf/ et corriger les erreurs éventuelles
- [ ] T027 Vérifier qu'aucun import pyscaf.preference_chain, pyscaf.tools, pyscaf.actions.manager ne reste dans le code
- [ ] T028 Mettre à jour README.md pour mentionner pyscaf-core comme dépendance

## Dependency Graph

Setup (Phase 1) → Core (Phase 2) → Nettoyage (Phase 3) → Tests (Phase 4) → Polish (Phase 5)

## Summary

- Total tasks: 28
- By priority: P0=18 (phases 1-3), P1=7 (phase 4), P2=3 (phase 5)
- Estimated effort: ~0.5 j/h (un développeur senior, tâche mécanique bien définie)
