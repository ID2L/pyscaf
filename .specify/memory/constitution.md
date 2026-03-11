# Project Constitution — pyscaf

## Project Principles

1. **Convention over configuration** — pyscaf provides sensible defaults so users can scaffold a complete Python project in one command, without having to configure everything manually.
2. **Plugin-first extensibility** — Every feature is an `Action` subclass, discovered dynamically at runtime. Adding a new capability means adding a new module; nothing else needs to change.
3. **Dependency-driven ordering** — Action execution order is computed automatically from declared dependencies (`depends`) and preferences (`run_preferably_after`). No hardcoded lists.
4. **Test-Driven Development (TDD)** — Every building block MUST have tests before or alongside implementation. No code is considered complete without corresponding test coverage. This applies to actions, preference chain logic, tools, and any new module.

## Governance

- Ratification Date: 2026-03-11
- Last Amended Date: 2026-03-11
- Constitution Version: 1.0.0

## Implementation

- Primary Language: Python 3.12+
- Package name on PyPI: `open-pyscaf`
- Internal package: `pyscaf` (located in `src/pyscaf/`)
- Build backend: Hatchling (`pyproject.toml`)
- Package manager: uv (also a runtime dependency — `uv>=0.10.8`)
- Code Standards: Ruff (rules B, C4, E, F, N, W, I, UP; line-length 120; src layout `src/`, `tests/`)
- Testing Requirements: pytest + pytest-cov; all tests in `tests/`; markers: cli, actions, manager, interactive, slow, integration, unit. **TDD is mandatory**: every new action, tool, or feature MUST ship with tests.
- Documentation Policy: Each action ships its own `README.md`; global README at repo root; inline docstrings on all public classes/methods

## Testing Strategy & Patterns

The project follows strict TDD. Three distinct testing patterns coexist, each tailored to the component being tested.

### Pattern 1 — Dynamic YAML Tests for Actions (`tests/actions/`)

Actions are tested via **YAML configuration files** that are auto-discovered at test time. This is the required pattern for all action tests.

**Framework files:**

| File | Role |
|---|---|
| `tests/actions/test_actions.py` | `ActionTestRunner` class + `discover_test_files()` + parametrised `test_action()` |
| `tests/actions/conftest.py` | `--action-filter` option for selective test execution |

**How it works:**

1. `discover_test_files()` scans all `tests/actions/<module>/*.yaml` files via `rglob("*.yaml")`.
2. Each YAML file is loaded by `ActionTestRunner`, which creates a temp directory, builds a CLI command from the YAML's `cli_arguments`, runs `pyscaf init`, then executes all `checks`.
3. Tests are parametrised: each YAML file becomes a separate pytest case with ID `<module>:<test_name>`.

**YAML structure:**

```yaml
cli_arguments:                    # Optional — omit for default behaviour
  positionals: ["init", "tmp"]    # Optional — defaults to ["init", "tmp_project"]
  options:
    versionning: true             # bool → --versionning / --no-versionning
    license: "mit"                # str → --license mit

checks:
  - name: "README exists"
    type: exist                   # exist | not_exist | contains | not_contains | custom
    file_path: "tmp_project/README.md"
  - name: "Has MIT header"
    type: contains
    file_path: "tmp_project/LICENSE"
    content: "MIT License"
  - name: "Custom validation"
    type: custom
    function_path: "tests.actions.custom_checks:my_check"
```

**Check types:**

| Type | Purpose | Required fields |
|---|---|---|
| `exist` | File/dir exists | `file_path` |
| `not_exist` | File/dir does NOT exist | `file_path` |
| `contains` | File contains substring | `file_path`, `content` |
| `not_contains` | File does NOT contain substring | `file_path`, `content` |
| `custom` | Runs a Python function `(temp_dir) → bool` | `function_path` |

**Run commands:**

```bash
pytest tests/actions/ -v                                  # All action tests
pytest tests/actions/ --action-filter="core" -v           # Only core module
pytest tests/actions/ --action-filter="core:test_author"  # Single test
```

**Requirement: every new Action MUST include at least:**
- `test_default.yaml` — tests the action with no specific CLI arguments
- One or more YAML files testing each meaningful option combination
- Negative tests (`not_exist`, `not_contains`) when applicable

**Existing test coverage per action:**

| Action | YAML files |
|---|---|
| core | `test_default`, `test_author`, `test_name_with_hyphen` |
| git | `test_default`, `test_disabled`, `test_no_versionning`, `test_with_remote` |
| license | `test_default`, `test_apache`, `test_bsd`, `test_gpl`, `test_mpl`, `test_unlicense` |
| documentation | `test_default`, `test_none`, `test_pdoc` |
| jupyter | `test_default`, `test_enabled`, `test_no_jupyter` |
| jupyter_tools | `test_default`, `test_disabled`, `test_enabled` |
| test | `test_default`, `test_enabled`, `test_no_testing`, `test_with_git` |
| semantic-release | `test_default`, `test_disabled`, `test_custom_project_name`, `test_gitlab`, `test_no_versionning` |

### Pattern 2 — Preference Chain Tests (`tests/preference_chain/`)

The preference chain has its own test suite with two layers:

**A) YAML Integration Tests — `test_preference_chain.py`**

Uses `PreferenceChainTestHelper` to load YAML dependency graphs, resolve them, and validate ordering.

- Helper methods: `resolve_dependencies_from_yaml(filename)`, `create_yaml_file(filename, deps)`
- Test data in `tests/preference_chain/test_data/*.yaml`
- Covers: simple linear, diamond, preferences, complex scenarios, circular detection, single nodes, multiple roots

**B) API Unit Tests — `test_execution_order.py`**

Tests `best_execution_order()` directly with `Node` objects (no YAML).

- Covers: linear chains, diamond, auto-after for single deps, multiple externals, circular detection, complex CI/CD-like scenarios, empty input, single node, invalid `after` field

**Validation patterns used:**

```python
assert result == ["A", "B", "C"]                           # Exact ordering
assert result.index("A") < result.index("B")               # Relative ordering
assert result[0] == "root"                                  # Position check
with pytest.raises(CircularDependencyError):                # Error detection
    best_execution_order(circular_nodes)
```

**Requirement:** any change to the preference chain algorithm MUST be covered by both a YAML integration test and an API unit test.

### Pattern 3 — Tool Unit Tests (`tests/tools/`)

Standalone `test_*.py` files with `tempfile.TemporaryDirectory` for isolation.

- `test_toml_merge.py` covers: simple merge, nested merge, list merge, overwrite, no-overwrite of unrelated keys
- Pattern: `write_toml()` → call function under test → `read_toml()` → assert

**Requirement:** any new tool in `src/pyscaf/tools/` MUST have a corresponding `tests/tools/test_<tool_name>.py`.

### General Testing Rules

1. **No code without tests** — TDD is the project's methodology. Write the test first, or at minimum alongside the implementation.
2. **One test = one behaviour** — Explicit test names, docstrings in English.
3. **Isolation** — All tests use `tempfile` or `tmp_path`; no side effects between tests.
4. **Cleanup** — Temporary files/directories are always cleaned up.
5. **Test structure mirrors source** — `tests/actions/` tests `src/pyscaf/actions/`, `tests/preference_chain/` tests `src/pyscaf/preference_chain/`, `tests/tools/` tests `src/pyscaf/tools/`.

## Architecture Overview

### Entry Point

`src/pyscaf/cli.py` — Click group `cli` with one subcommand `init`.

```
pyscaf init [--interactive] [--no-install] <project_name> [dynamic options...]
```

Dynamic CLI options are collected at startup by calling `discover_actions()` and ordering them via the preference chain. Each `Action` subclass declares its own `cli_options: list[CLIOption]`.

### Core Abstractions

#### `Action` (abstract base class) — `src/pyscaf/actions/__init__.py:126`

The foundational contract every feature must implement.

| Attribute / Method | Role |
|---|---|
| `depends: set[str]` | Hard dependencies on other action IDs (class-level) |
| `run_preferably_after: str \| None` | Soft ordering hint (class-level) |
| `cli_options: list[CLIOption]` | Options this action exposes to the CLI & interactive mode |
| `skeleton(context) → dict[Path, str\|None]` | Declares files/dirs to create. `None` value = directory, string = file content |
| `init(context)` | Merges the action's `config.toml` into the project's `pyproject.toml` (default impl) |
| `install(context)` | Runs post-init commands (e.g., `uv sync`, kernel registration) |
| `activate(context) → bool` | Guards whether the action is active for the current context (default: `True`) |
| `create_skeleton(context)` | Materialises the dict returned by `skeleton()` on disk |

Validation rule (enforced in `__init_subclass__`): if `len(depends) > 1` and `run_preferably_after` is `None`, a `ValueError` is raised at class definition time.

#### `CLIOption` (Pydantic model) — `src/pyscaf/actions/__init__.py:56`

Describes a single CLI flag/argument. Key fields:

- `name` — CLI flag name, e.g. `--author`
- `type` — `"str"`, `"bool"`, `"int"`, or `"choice"`
- `choices: list[ChoiceOption] | None` — used when `type == "choice"`
- `default` — scalar or callable (e.g., `get_local_git_author`)
- `postfill_hook: Callable[[dict], dict] | None` — called after the user provides a value; used to derive dependent context keys (e.g., `postfill_remote_url` detects the git host from the URL)
- `multiple: bool | None` — enables checkbox (multi-select) in interactive mode

#### `ChoiceOption` (Pydantic model) — `src/pyscaf/actions/__init__.py:21`

Separates three concerns for choice-type options:

- `key` — stored in context and used on the CLI
- `display` — shown in interactive (questionary) prompts
- `value` — the actual value passed to business logic (e.g., a template filename)

### Dependency Resolution — `src/pyscaf/preference_chain/`

The preference chain is a self-contained sub-package that computes the optimal execution order for a set of nodes with dependencies and ordering preferences.

#### Data model — `src/pyscaf/preference_chain/model.py`

| Class | Role |
|---|---|
| `Node` | `id`, `depends: set[str]`, `after: str\|None`. `external_dependencies` property = `depends - {after}` |
| `ExtendedNode(Node)` | Adds `referenced_by: set[str]` (reverse dependencies, computed by `extend_nodes`) |
| `ChainLink` | A sorted list of `ExtendedNode`s forming a linear chain. Exposes `ids`, `external_dependencies`, `depends`, `referenced_by` |

#### Algorithm — `src/pyscaf/preference_chain/chain.py`

1. **`extend_nodes(tree)`** — Converts `Node` → `ExtendedNode`, populating `referenced_by` by scanning all `depends` sets.
2. **`build_chains(extended_nodes)`** — Groups nodes into `ChainLink`s by repeatedly calling `update_chains` (attach node to existing chain) and `merge_chains` (merge two chains). Detects circular dependencies.
3. **`compute_all_resolution_pathes(chains)`** — Generates all permutations of chains and filters only those where each chain's `depends` are fulfilled by previous chains.
4. **`compute_path_score(path)`** — Scores a path by counting "after" mismatches between consecutive chains (fewer mismatches = higher score).
5. **`best_execution_order(nodes)`** — Public API: returns the flat list of node IDs in the optimal order.

#### `DependencyTreeWalker` — `src/pyscaf/preference_chain/tree_walker.py:6`

A utility class that builds a tree view from a root node following `after` links, used for debugging/visualisation.

### `ActionManager` — `src/pyscaf/actions/manager.py:27`

Orchestrates the entire project creation lifecycle:

1. `__init__` → calls `_determine_actions()` which runs the full preference-chain algorithm and instantiates actions in optimal order.
2. `run_postfill_hooks(context)` → calls each active action's `postfill_hook` for already-provided context values.
3. `ask_interactive_questions(context)` → uses `questionary` to prompt the user for missing values, then calls `postfill_hook`.
4. `create_project()` → three sequential passes:
   - **Pass 1 — skeletons**: calls `action.create_skeleton(context)` for every active action.
   - **Pass 2 — init**: calls `action.init(context)` for every active action.
   - **Pass 3 — install**: calls `action.install(context)` unless `--no-install` was passed.

### Concrete Actions

| Action class | Module | `depends` | `run_preferably_after` | Key behaviour |
|---|---|---|---|---|
| `CoreAction` | `actions/core/__init__.py:29` | `{}` (root) | `None` | Runs `uv init --bare --lib --no-workspace`, writes authors into `pyproject.toml`, installs VSCode Ruff extension |
| `GitAction` | `actions/git/__init__.py:39` | `{"core"}` | `"core"` | `git init`, optional remote, initial commit; `postfill_remote_url` auto-detects GitHub/GitLab from URL |
| `LicenseAction` | `actions/license/__init__.py:39` | `{"core"}` | `"core"` | Copies a license template (MIT, Apache-2.0, GPL-3.0, BSD-3-Clause, MPL-2.0, Unlicense) |
| `DocumentationAction` | `actions/documentation/__init__.py:11` | `{"core"}` | `"core"` | Optionally sets up pdoc; copies parse scripts |
| `JupyterAction` | `actions/jupyter/__init__.py:19` | `{"core","git"}` | `"git"` | Creates `notebooks/` directory; registers a project-specific Jupyter kernel via `uv run ipykernel install` |
| `JupyterToolsAction` | `actions/jupyter_tools/__init__.py` | see module | see module | Additional Jupyter utilities (notebook-to-HTML/PDF, execute, py-to-notebook) |
| `TestAction` | `actions/test/__init__.py:16` | `{"core","git"}` | `"git"` | Creates `tests/` structure with example test; validates with `uv run pytest --version` |
| `SemanticReleaseAction` | `actions/semantic-release/__init__.py` | see module | see module | Copies GitHub Actions workflows for semantic-release CD pipeline |

### Tools — `src/pyscaf/tools/`

| Module | Role |
|---|---|
| `toml_merge.py` | `merge_toml_files(input, output)` — recursive deep-merge of TOML files using tomlkit, preserving comments. Used by `Action.init()` to merge each action's `config.toml` into the project's `pyproject.toml`. |
| `format_toml.py` | Reformats a TOML file after merging. |

### Action Discovery — `src/pyscaf/actions/__init__.py:235`

`discover_actions()` uses `pkgutil.iter_modules` to scan the `actions/` package directory and imports each sub-module, collecting all classes that are `Action` subclasses (excluding `Action` itself and internal modules `base`, `manager`, `__pycache__`).

### Context Dictionary

The `context` dict is the single shared mutable state flowing through the entire pipeline. Keys are derived from CLI option names via `cli_option_to_key` (strip leading `--`, replace `-` with `_`). Example: `--remote-url` → `remote_url`.

Key reserved keys:

| Key | Source | Meaning |
|---|---|---|
| `project_name` | CLI argument | Name of the project being scaffolded |
| `interactive` | `--interactive` flag | Whether to prompt the user |
| `no_install` | `--no-install` flag | Skip `install()` pass |
| `author` | CoreAction | Author string (`Name <email>`) |
| `versionning` | GitAction | Whether git is enabled |
| `remote_url` | GitAction | Git remote URL |
| `git_host` | GitAction (postfill) | `"github"` or `"gitlab"` |
| `license` | LicenseAction | License key (e.g., `"mit"`) |
| `jupyter` | JupyterAction | Whether to include Jupyter |
| `testing` | TestAction | Whether to include pytest |
| `documentation` | DocumentationAction | Documentation system key |
