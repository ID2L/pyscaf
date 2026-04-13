# Bug Investigation Report: Git questions shown after answering "No" to versionning

## Executive Summary

- **Bug**: When running `pyscaf init --interactive`, answering "No" to "Does this project will be versionned with git?" still prompts for "Git remote url?" and "Git host?", and ultimately initializes a git repository.
- **Impact**: User intent is ignored — the project gets git-initialized despite explicitly declining.
- **Root cause**: The `--remote-url` and `--git-host` CLI options in `GitAction` are missing `visible_when` guards, and their `postfill_hook` callbacks override `versionning` back to `True`.

## Reproduction Details

### Steps to reproduce

```bash
uv run pyscaf init playground/my-project --no-install --interactive
```

Answer the prompts as follows:
1. Author: (any value)
2. Documentation: None
3. **"Does this project will be versionned with git?" → No**
4. "Git remote url?" → (this question should NOT appear)
5. "Git host?" → (this question should NOT appear)

### Expected behavior

After answering "No" to git versionning:
- No further git-related questions should be asked
- No `.git/` directory should be created
- No `.gitignore` or `README.md` from `GitAction` should be generated

### Actual behavior

- "Git remote url?" and "Git host?" are still asked
- A git repository is initialized (`Initialized empty Git repository`)
- Git-related files are created

## Code Path Analysis

### Execution flow

```
pyscaf.main:main()
  → pyscaf_core.cli:build_cli()
    → init() command
      → ActionManager(project_name, context, discover=discover_actions)
      → manager.run_postfill_hooks(context)
      → manager.ask_interactive_questions(context)   ← BUG HERE
      → manager.create_project()
```

### Critical code path in `ask_interactive_questions()`

File: `pyscaf_core/actions/manager.py` lines 86-143

```python
def ask_interactive_questions(self, context: dict) -> dict:
    for action in self.actions:
        if action.activate(context):          # ← checked ONCE for all options
            for opt in action.cli_options:     # ← iterates --versionning, --remote-url, --git-host
                context_key = cli_option_to_key(opt)
                if context.get(context_key) is not None:
                    continue
                if opt.visible_when and not opt.visible_when(context):  # ← mechanism exists!
                    continue
                # ... ask question, set context[context_key], run postfill_hook
```

### GitAction CLI options (the bug location)

File: `src/pyscaf/actions/git/__init__.py` lines 41-65

```python
cli_options = [
    CLIOption(
        name="--versionning",
        type="bool",
        prompt="Does this project will be versionned with git ?",
        default=True,
    ),
    CLIOption(
        name="--remote-url",
        type="str",
        prompt="Git remote url ?",
        postfill_hook=postfill_remote_url,
        # ← MISSING: visible_when=lambda ctx: ctx.get("versionning") is not False
    ),
    CLIOption(
        name="--git-host",
        type="choice",
        prompt="Git host ?",
        choices=GIT_HOST_CHOICES,
        default=0,
        postfill_hook=postfill_git_host,
        # ← MISSING: visible_when=lambda ctx: ctx.get("versionning") is not False
    ),
]
```

## Identified Anomalies

### Anomaly 1: Missing `visible_when` on `--remote-url` and `--git-host`

- **Evidence**: The `CLIOption` model supports `visible_when: Callable[[dict], bool] | None` (pyscaf_core/actions/__init__.py:38), and `ask_interactive_questions()` checks it (manager.py:94-95). But `--remote-url` and `--git-host` do not define it.
- **Impact**: Questions are shown even when `context["versionning"]` is `False`.

### Anomaly 2: `postfill_hook` overrides user choice

- **Evidence**: `postfill_remote_url` and `postfill_git_host` both set `context["versionning"] = True` unconditionally (git/__init__.py lines 21, 32).
- **Impact**: Even if a future fix skips the questions, providing `--remote-url` or `--git-host` via CLI flags would still override a `--no-versionning` flag. The postfill hooks are designed for the case where providing a remote URL implies git usage — but they should not fight an explicit `--no-versionning`.

## Root Cause Analysis

**Primary root cause**: `--remote-url` and `--git-host` options lack `visible_when` guards that check whether `versionning` is enabled.

**Contributing factor**: The `postfill_hook` on both options force `versionning=True`, which overrides the user's explicit "No" answer if those questions are reached.

## Recommendations

### Fix (in `src/pyscaf/actions/git/__init__.py`)

1. Add `visible_when=lambda ctx: ctx.get("versionning") is not False` to both `--remote-url` and `--git-host` CLIOption definitions.
2. This ensures `ask_interactive_questions()` skips these prompts when versionning is False.
3. The `postfill_hook` behavior is acceptable for the CLI-flag path (where providing `--remote-url` should imply git), so no change needed there.

### Scope

- **Entirely within this project** (`src/pyscaf/actions/git/__init__.py`)
- No changes needed in `pyscaf_core`

## Status Tracking

- [x] Investigation complete
- [x] Root cause identified
- [ ] Fix implemented
- [ ] Testing completed
- [ ] Bug resolved
