# AGENT.md — pyscaf

> **Mandatory:** This file must be kept up to date after every significant change to the codebase. It is the primary navigation document for AI agents working on this repository.

Full architecture reference: [`.specify/memory/constitution.md`](.specify/memory/constitution.md)

---

## What is pyscaf?

`pyscaf` (published on PyPI as `open-pyscaf`) is a CLI tool that scaffolds complete, modern Python projects in one command. It runs `uv init`, configures linting (ruff), testing (pytest), git, Jupyter, documentation (pdoc), licensing, and semantic-release — all driven by a plugin architecture.

- Entry point: `src/pyscaf/cli.py:181` (`main()` → `cli()` Click group → `init` subcommand)
- Package version: `src/pyscaf/__init__.py:5` (`__version__ = "1.6.0"`)
- PyPI package: `open-pyscaf` (defined in `pyproject.toml:2`)

---

## Key Files & Line References

### CLI layer

| File | Lines | Description |
|---|---|---|
| `src/pyscaf/cli.py` | 1–191 | Click CLI: `cli` group, `init` command, dynamic option injection |
| `src/pyscaf/cli.py` | 29–51 | `collect_cli_options()` — discovers actions, computes order, collects CLI options |
| `src/pyscaf/cli.py` | 105–136 | `add_dynamic_options()` — injects each action's `cli_options` into the Click command |
| `src/pyscaf/cli.py` | 161–178 | `init()` — entry point for project creation: fills context, runs hooks, asks questions, calls `ActionManager` |

### Abstract base class — Action

| File | Lines | Description |
|---|---|---|
| `src/pyscaf/actions/__init__.py` | 126–232 | `Action` abstract base class |
| `src/pyscaf/actions/__init__.py` | 137–140 | Class-level declarations: `depends`, `run_preferably_after`, `cli_options` |
| `src/pyscaf/actions/__init__.py` | 142–145 | `__init_subclass__` validation: enforces `run_preferably_after` when `len(depends) > 1` |
| `src/pyscaf/actions/__init__.py` | 150–163 | `skeleton()` — returns `dict[Path, str\|None]`; override in subclasses |
| `src/pyscaf/actions/__init__.py` | 165–179 | `init()` — default: merges action's `config.toml` into project's `pyproject.toml` |
| `src/pyscaf/actions/__init__.py` | 182–191 | `install()` — override to run post-init commands |
| `src/pyscaf/actions/__init__.py` | 193–225 | `create_skeleton()` — materialises the `skeleton()` dict on disk |
| `src/pyscaf/actions/__init__.py` | 227–232 | `activate()` — guard; returns `True` by default |

### Pydantic models — CLI options

| File | Lines | Description |
|---|---|---|
| `src/pyscaf/actions/__init__.py` | 21–53 | `ChoiceOption` — key/display/value separation for choice-type options |
| `src/pyscaf/actions/__init__.py` | 56–123 | `CLIOption` — full CLI option descriptor with postfill hooks |

### Action discovery

| File | Lines | Description |
|---|---|---|
| `src/pyscaf/actions/__init__.py` | 235–250 | `discover_actions()` — dynamic import of all `Action` subclasses via `pkgutil.iter_modules` |
| `src/pyscaf/actions/cli_option_to_key.py` | 1–5 | `cli_option_to_key()` — converts `--remote-url` → `remote_url` |

### Action Manager (orchestrator)

| File | Lines | Description |
|---|---|---|
| `src/pyscaf/actions/manager.py` | 27–207 | `ActionManager` class |
| `src/pyscaf/actions/manager.py` | 30–44 | `__init__` — sets `project_path`, calls `_determine_actions()` |
| `src/pyscaf/actions/manager.py` | 46–100 | `_determine_actions()` — runs full preference-chain algorithm, instantiates actions in optimal order |
| `src/pyscaf/actions/manager.py` | 102–112 | `run_postfill_hooks()` — applies `postfill_hook` for pre-provided context values |
| `src/pyscaf/actions/manager.py` | 114–170 | `ask_interactive_questions()` — questionary prompts for missing context values |
| `src/pyscaf/actions/manager.py` | 172–207 | `create_project()` — three-pass execution: skeleton → init → install |

### Dependency resolution (preference chain)

| File | Lines | Description |
|---|---|---|
| `src/pyscaf/preference_chain/model.py` | 8–11 | `Node` — `id`, `depends`, `after`, `external_dependencies` property |
| `src/pyscaf/preference_chain/model.py` | 18–19 | `ExtendedNode(Node)` — adds `referenced_by` set |
| `src/pyscaf/preference_chain/model.py` | 22–43 | `ChainLink` — linear sequence of `ExtendedNode`s; aggregates `ids`, `external_dependencies`, `depends`, `referenced_by` |
| `src/pyscaf/preference_chain/chain.py` | 11–34 | `extend_nodes()` — populates `referenced_by` (reverse deps) |
| `src/pyscaf/preference_chain/chain.py` | 37–77 | `update_chains()` — attaches a node to an existing chain or creates a new one |
| `src/pyscaf/preference_chain/chain.py` | 80–123 | `merge_chains()` — merges two compatible chains into one |
| `src/pyscaf/preference_chain/chain.py` | 126–146 | `build_chains()` — full chain construction with circular dependency detection |
| `src/pyscaf/preference_chain/chain.py` | 149–177 | `compute_all_resolution_pathes()` — permutation filter for valid ordering |
| `src/pyscaf/preference_chain/chain.py` | 180–191 | `compute_path_score()` — scores a path by "after" alignment |
| `src/pyscaf/preference_chain/__init__.py` | 20–83 | `best_execution_order()` — public API returning flat list of node IDs |
| `src/pyscaf/preference_chain/tree_walker.py` | 6–76 | `DependencyTreeWalker` — debug utility for visualising the dependency tree |

### Concrete actions

| File | Lines | Class | depends | Notes |
|---|---|---|---|---|
| `src/pyscaf/actions/core/__init__.py` | 29–179 | `CoreAction` | `{}` | Root action: `uv init --bare --lib`, writes `authors` in pyproject.toml, `uv sync`, installs Ruff VSCode ext |
| `src/pyscaf/actions/git/__init__.py` | 39–177 | `GitAction` | `{"core"}` | `git init`, optional remote; `postfill_remote_url` (line 23) auto-detects host from URL |
| `src/pyscaf/actions/license/__init__.py` | 39–75 | `LicenseAction` | `{"core"}` | Copies license template; 6 choices: MIT, Apache-2.0, GPL-3.0, BSD-3-Clause, MPL-2.0, Unlicense |
| `src/pyscaf/actions/documentation/__init__.py` | 11–69 | `DocumentationAction` | `{"core"}` | Optional pdoc setup; copies `scripts/parse_doc.py` |
| `src/pyscaf/actions/jupyter/__init__.py` | 19–123 | `JupyterAction` | `{"core","git"}` | Creates `notebooks/`; registers ipykernel via `uv run ipykernel install` |
| `src/pyscaf/actions/test/__init__.py` | 16–121 | `TestAction` | `{"core","git"}` | Creates `tests/`, example test from template; validates with `uv run pytest --version` |
| `src/pyscaf/actions/semantic-release/__init__.py` | — | `SemanticReleaseAction` | see file | Copies GitHub Actions workflow files for CD |
| `src/pyscaf/actions/jupyter_tools/__init__.py` | — | `JupyterToolsAction` | see file | Scripts: execute_notebook, notebook_to_html/pdf, py_to_notebook |

### Shared tools

| File | Lines | Description |
|---|---|---|
| `src/pyscaf/tools/toml_merge.py` | 6–49 | `merge_toml_files()` — deep-merges TOML files with tomlkit, preserves comments |
| `src/pyscaf/tools/format_toml.py` | — | `format_toml()` — reformats a TOML file after merging |

---

## Dependency Graph (action execution order)

```
core  (root, no deps)
├── git          (depends: core)
│   ├── jupyter  (depends: core + git)
│   └── test     (depends: core + git)
├── license      (depends: core)
├── documentation (depends: core)
└── semantic-release / jupyter_tools  (see each module)
```

The actual order is computed at runtime by the preference-chain algorithm — the graph above is illustrative.

---

## Context Dictionary — Key Conventions

- All context keys derived from CLI flags via `cli_option_to_key`: `--remote-url` → `remote_url`
- `None` in context means "not yet set"; `False` means "explicitly disabled"
- `postfill_hook`s can add/overwrite keys derived from user input (e.g., `versionning=True` set by `postfill_remote_url`)

---

## TDD — Testing is Mandatory

**This project follows strict Test-Driven Development. Every new action, tool, feature, or algorithm change MUST ship with tests.** No PR is complete without test coverage.

Full testing strategy details: see [constitution.md — Testing Strategy & Patterns](.specify/memory/constitution.md#testing-strategy--patterns).

### Test Architecture at a Glance

```
tests/
├── actions/                        # Dynamic YAML tests for actions
│   ├── test_actions.py             # ActionTestRunner + discover_test_files() + parametrised test_action()
│   ├── conftest.py                 # --action-filter pytest option
│   ├── core/test_*.yaml            # One YAML per test case
│   ├── git/test_*.yaml
│   ├── license/test_*.yaml
│   └── ...
├── preference_chain/               # Preference chain tests
│   ├── test_preference_chain.py    # YAML integration tests (PreferenceChainTestHelper)
│   ├── test_execution_order.py     # API unit tests (best_execution_order with Node objects)
│   └── test_data/*.yaml
└── tools/
    └── test_toml_merge.py          # Tool unit tests (tempfile-based)
```

### Three Test Patterns

| Pattern | Where | How | When to use |
|---|---|---|---|
| **Dynamic YAML** | `tests/actions/<module>/test_*.yaml` | YAML defines `cli_arguments` + `checks`; `ActionTestRunner` runs pyscaf in a temp dir and validates | Any new or modified **Action** |
| **Preference chain** | `tests/preference_chain/` | `PreferenceChainTestHelper` for YAML integration + direct `best_execution_order()` API tests | Any change to the **dependency resolution** algorithm |
| **Tool unit tests** | `tests/tools/test_<name>.py` | Classic pytest with `tempfile.TemporaryDirectory` | Any new or modified **tool** in `src/pyscaf/tools/` |

### YAML Test Format for Actions (quick reference)

```yaml
cli_arguments:                        # Optional — omit for default behaviour
  options:
    versionning: true                 # --versionning
    license: "mit"                    # --license mit

checks:
  - name: "README exists"
    type: exist                       # exist | not_exist | contains | not_contains | custom
    file_path: "tmp_project/README.md"
  - name: "Has MIT header"
    type: contains
    file_path: "tmp_project/LICENSE"
    content: "MIT License"
```

### Action Test Files Reference

| Action | Tests (in `tests/actions/`) |
|---|---|
| `core` | `test_default.yaml`, `test_author.yaml`, `test_name_with_hyphen.yaml` |
| `git` | `test_default.yaml`, `test_disabled.yaml`, `test_no_versionning.yaml`, `test_with_remote.yaml` |
| `license` | `test_default.yaml`, `test_apache.yaml`, `test_bsd.yaml`, `test_gpl.yaml`, `test_mpl.yaml`, `test_unlicense.yaml` |
| `documentation` | `test_default.yaml`, `test_none.yaml`, `test_pdoc.yaml` |
| `jupyter` | `test_default.yaml`, `test_enabled.yaml`, `test_no_jupyter.yaml` |
| `jupyter_tools` | `test_default.yaml`, `test_disabled.yaml`, `test_enabled.yaml` |
| `test` | `test_default.yaml`, `test_enabled.yaml`, `test_no_testing.yaml`, `test_with_git.yaml` |
| `semantic-release` | `test_default.yaml`, `test_disabled.yaml`, `test_custom_project_name.yaml`, `test_gitlab.yaml`, `test_no_versionning.yaml` |

### Key Test Files & Line References

| File | Lines | Description |
|---|---|---|
| `tests/actions/test_actions.py` | 19–35 | `CheckResult` / `TestResult` TypedDicts |
| `tests/actions/test_actions.py` | 37–213 | `ActionTestRunner` — loads YAML, builds CLI cmd, runs pyscaf, executes checks |
| `tests/actions/test_actions.py` | 65–93 | `_build_cli_command()` — translates YAML options to CLI flags |
| `tests/actions/test_actions.py` | 143–183 | `_run_checks()` — dispatches check types (exist/contains/custom) |
| `tests/actions/test_actions.py` | 216–239 | `discover_test_files()` — rglobs `*.yaml` under `tests/actions/` |
| `tests/actions/test_actions.py` | 260–301 | `test_action()` — parametrised pytest entry point |
| `tests/actions/conftest.py` | 15–24 | `pytest_addoption()` — adds `--action-filter` |
| `tests/actions/conftest.py` | 27–75 | `pytest_collection_modifyitems()` — filters by `module:test_name` |
| `tests/preference_chain/test_preference_chain.py` | 20–89 | `PreferenceChainTestHelper` — resolves YAML deps, creates test data |
| `tests/preference_chain/test_preference_chain.py` | 92–265 | `TestPreferenceChainIntegration` — 7 test methods (linear, diamond, preference, complex, circular, single, multi-root) |
| `tests/preference_chain/test_execution_order.py` | 11–187 | `TestBestExecutionOrder` — 10 API tests with `Node` objects |
| `tests/tools/test_toml_merge.py` | 1–79 | 5 test functions for `merge_toml_files` |

### Run Commands

```bash
# All tests
uv run pytest

# Action tests only
uv run pytest tests/actions/ -v

# Single action module
uv run pytest tests/actions/ --action-filter="core" -v

# Single action test
uv run pytest tests/actions/ --action-filter="core:test_author" -v

# Preference chain tests
uv run pytest tests/preference_chain/ -v

# Tool tests
uv run pytest tests/tools/ -v

# With debug logging
uv run pytest tests/preference_chain/ -s --log-cli-level=DEBUG
```

---

## Development Commands

```bash
# Install dev dependencies
uv sync

# Run all tests (mandatory before any PR)
uv run pytest

# Lint & format
uv run ruff check src/ tests/
uv run ruff format src/ tests/

# Build package
uv build

# Run pyscaf locally
uv run pyscaf init --interactive my-project
```

---

## How to Add a New Action (Checklist)

1. **Write tests first (TDD)**: Create `tests/actions/<my_feature>/test_default.yaml` + additional YAML test files for each option combination
2. Create `src/pyscaf/actions/<my_feature>/__init__.py`
3. Define a class inheriting from `Action`
4. Declare `depends`, `run_preferably_after`, and `cli_options` at class level
5. Implement `skeleton()`, `init()` (or keep default for `config.toml` merge), `install()`, and optionally `activate()`
6. Optionally add a `config.toml` in the same directory to inject pyproject.toml settings
7. `discover_actions()` will pick it up automatically — no registration needed
8. **Verify**: `uv run pytest tests/actions/ --action-filter="<my_feature>" -v` must pass
9. Update this `AGENT.md` with the new action and its test files

## How to Add a New Tool (Checklist)

1. **Write tests first (TDD)**: Create `tests/tools/test_<tool_name>.py` using `tempfile.TemporaryDirectory`
2. Create `src/pyscaf/tools/<tool_name>.py`
3. **Verify**: `uv run pytest tests/tools/test_<tool_name>.py -v` must pass
4. Update this `AGENT.md`

## How to Modify the Preference Chain (Checklist)

1. **Write tests first (TDD)**: Add YAML test data in `tests/preference_chain/test_data/` + test method in `TestPreferenceChainIntegration` + API test in `TestBestExecutionOrder`
2. Implement the change in `src/pyscaf/preference_chain/`
3. **Verify**: `uv run pytest tests/preference_chain/ -v` must pass
4. Update this `AGENT.md`
