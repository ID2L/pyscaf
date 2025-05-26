"""
Interactive mode for pyscaf.
"""
import questionary
from rich.console import Console

from pyscaf.actions import discover_actions
from pyscaf.preference_chain.topologic_tree import best_execution_order

console = Console()



def get_dynamic_context(project_name: str) -> dict:
    """
    Ask all questions dynamically based on cli_options of actions, in optimal order.
    Supports types: str, int, bool, choice, multiple.
    Returns a context dict with all answers.
    """
    action_classes = discover_actions()
    deps = []
    action_class_by_id = {}
    for action_cls in action_classes:
        action_id = action_cls.__name__.replace('Action', '').lower()
        deps.append({
            "id": action_id,
            "depends": getattr(action_cls, "depends", []),
            "after": getattr(action_cls, "run_preferably_after", None)
        })
        action_class_by_id[action_id] = action_cls
    order = best_execution_order([
        {
            "id": d["id"],
            "fullfilled": [d["id"]],
            "external": d["depends"] or []
        }
        for d in deps
    ])
    context = {"project_name": project_name}
    for action_id in order:
        action_cls = action_class_by_id[action_id]
        for opt in getattr(action_cls, "cli_options", []):
            name = opt.name.lstrip("-").replace("-", "_")
            prompt = opt.prompt or name
            default = opt.default() if callable(opt.default) else opt.default
            if opt.type == "bool":
                answer = questionary.confirm(prompt, default=bool(default)).ask()
            elif opt.type == "int":
                answer = questionary.text(prompt, default=str(default) if default is not None else None).ask()
                answer = int(answer) if answer is not None else None
            elif opt.type == "choice" and opt.choices:
                if opt.multiple:
                    answer = questionary.checkbox(prompt, choices=opt.choices, default=default).ask()
                else:
                    answer = questionary.select(prompt, choices=opt.choices, default=default).ask()
            else:  # str or fallback
                answer = questionary.text(prompt, default=default).ask()
            context[name] = answer
    return context 