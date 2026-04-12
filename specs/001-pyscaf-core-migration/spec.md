# Feature Specification: Migration vers pyscaf-core

**Feature Branch**: `001-pyscaf-core-migration`
**Created**: 2026-04-12
**Status**: Draft
**Input**: User description: "Le coeur du scaffolder a été isolé dans le package pyscaf-core. Il faut réécrire ce package afin qu'il ait comme dépendance le pyscaf-core, et refactorer en fonction."

## User Scenarios & Testing

### User Story 1 — Le CLI `pyscaf init` fonctionne identiquement (Priority: P0)

L'utilisateur final ne doit percevoir aucun changement de comportement. La commande `pyscaf init <project_name>` (interactive et non-interactive) doit produire exactement la même structure de projet qu'avant.

**Why this priority**: C'est la raison d'être du package — toute régression ici est bloquante.
**Independent Test**: `pyscaf init myproject --no-install` puis vérifier la structure de sortie.

**Acceptance Scenarios**:

1. **Given** pyscaf est installé avec pyscaf-core comme dépendance, **When** `pyscaf init myproject --no-install`, **Then** la structure de répertoires et fichiers générée est identique à la version pré-migration.
2. **Given** pyscaf est installé, **When** `pyscaf --version`, **Then** la version s'affiche correctement.
3. **Given** pyscaf est installé, **When** `pyscaf init --help`, **Then** toutes les options dynamiques des actions apparaissent.

### User Story 2 — Les actions concrètes sont découvertes via le plugin system (Priority: P0)

Les 8 actions concrètes (core, git, jupyter, jupyter_tools, documentation, license, semantic-release, test) doivent être découvertes via le système de plugins entry-points de pyscaf-core.

**Why this priority**: Sans découverte des actions, rien ne fonctionne.
**Independent Test**: Appel `discover_actions()` et vérification du nombre et type des actions retournées.

**Acceptance Scenarios**:

1. **Given** pyscaf est installé, **When** on appelle `discover_actions()`, **Then** 8 classes Action sont retournées.
2. **Given** pyscaf est installé via entry-points, **When** pyscaf-core appelle `discover_actions_from_entry_points()`, **Then** les mêmes 8 actions sont découvertes.

### User Story 3 — Les tests YAML existants passent via le framework de test pyscaf-core (Priority: P1)

Les tests YAML existants dans `tests/actions/` doivent être exécutés par le framework de test `pyscaf_core.testing`.

**Why this priority**: Les tests garantissent la non-régression.
**Independent Test**: `pytest tests/` doit passer sans erreur.

**Acceptance Scenarios**:

1. **Given** les fixtures YAML existent, **When** `pytest` est exécuté, **Then** tous les tests YAML passent.
2. **Given** le plugin pytest `pyscaf_core.testing` est actif, **When** `create_yaml_tests(entry_point_name="pyscaf")` est appelé, **Then** les tests sont générés dynamiquement.

### Edge Cases

- Que se passe-t-il si pyscaf-core n'est pas installé ? → Erreur d'import claire au lancement.
- Que se passe-t-il si le dossier `semantic-release` contient un tiret dans le nom de module ? → Le discover via `pkgutil` le gère déjà (pattern existant conservé).

## Requirements

### Functional Requirements

- **FR-001**: Le package `open-pyscaf` DOIT déclarer `pyscaf-core` comme dépendance runtime.
- **FR-002**: Le code framework (Action, CLIOption, ChoiceOption, ActionManager, preference_chain, tools) DOIT être supprimé de `src/pyscaf/` et importé depuis `pyscaf_core`.
- **FR-003**: Les 8 actions concrètes DOIVENT rester dans `src/pyscaf/actions/` et importer `Action`, `CLIOption`, `ChoiceOption` depuis `pyscaf_core`.
- **FR-004**: Le CLI DOIT utiliser `build_cli()` et `make_main()` de `pyscaf_core` au lieu du code CLI monolithique actuel.
- **FR-005**: Les actions DOIVENT être exposées via `[project.entry-points."pyscaf_core.plugins"]` dans `pyproject.toml`.
- **FR-006**: Les tests YAML DOIVENT être exposés via `[project.entry-points."pyscaf_core.test_yamls"]`.
- **FR-007**: Un module `testing.py` DOIT fournir un `ActionTestConfig` pour les tests YAML.
- **FR-008**: Le module `cli_option_to_key.py` DOIT être supprimé (la fonction existe dans `pyscaf_core`).
- **FR-009**: Les modules `preference_chain/` et `tools/` DOIVENT être entièrement supprimés.
- **FR-010**: Les `print()` et `console.print()` directs dans les actions DOIVENT être remplacés par `logging.getLogger()`.

### Key Entities

- **Action** (from pyscaf_core): Classe de base pour les actions de scaffolding.
- **ActionManager** (from pyscaf_core): Orchestrateur des actions avec résolution de dépendances.
- **CLIOption / ChoiceOption** (from pyscaf_core): Modèles Pydantic pour les options CLI.
- **ActionTestConfig** (from pyscaf_core.testing): Configuration pour les tests YAML.

## Success Criteria

- **SC-001**: `pyscaf init myproject --no-install` produit la même arborescence qu'avant la migration.
- **SC-002**: Les 8 actions concrètes sont découvertes (test programmatique).
- **SC-003**: `pyscaf --version` et `pyscaf init --help` fonctionnent sans erreur.
- **SC-004**: 100% des tests YAML existants passent.
- **SC-005**: Aucun import de modules internes framework (`pyscaf.preference_chain`, `pyscaf.tools`, `pyscaf.actions.manager`) ne subsiste.
- **SC-006**: Le nombre de fichiers Python sous `src/pyscaf/` diminue d'au moins 10 fichiers (suppression du framework).

## Assumptions

- `pyscaf-core` version >= 0.2.1 est disponible (publié sur PyPI ou installable depuis le workspace).
- Le naming du package Python installable reste `pyscaf_core` (avec underscore).
- Le nom du package distribué reste `open-pyscaf`.
- La commande CLI reste `pyscaf`.
