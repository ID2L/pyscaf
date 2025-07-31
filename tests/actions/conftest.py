# conftest.py

# Import discover_test_files from your test_actions.py
# Assuming conftest.py is at the root or a level above tests/actions
# Adjust the import path as needed based on your project structure
# For example, if conftest.py is in 'tests/actions', you'd do:
# from test_actions import discover_test_files
# If conftest.py is at the project root and test_actions.py is in tests/actions, you'd do:
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "tests" / "actions"))


def pytest_addoption(parser):
    """Adds custom command-line options for test filtering."""
    group = parser.getgroup("pyscaf-action-tests", "PyScaf Action Test Filtering")

    group.addoption(
        "--action-filter",
        action="store",
        default=None,
        help="Filter action tests by module:test_name (e.g., 'core:test_author')",
    )


def pytest_collection_modifyitems(config, items):
    """Modifies the collected test items based on custom filters."""
    # module_filter = config.getoption("--module")
    # test_name_filter = config.getoption("--test-name")
    action_filter = config.getoption("--action-filter")

    # Initialize filters to None by default
    module_filter = None
    test_name_filter = None

    if action_filter:
        if ":" in action_filter:
            module_filter, test_name_filter = action_filter.split(":", 1)
        else:
            module_filter = action_filter
            test_name_filter = (
                None  # Ensure test_name_filter is cleared if only module is provided
            )

    # If no filters are provided, return early
    if not module_filter and not test_name_filter:
        return

    selected_items = []
    deselected_items = []

    for item in items:
        # Check if the test item is from your test_actions.py and uses the parametrize ID
        # The test ID is usually available as item.callspec.id for parametrized tests
        if hasattr(item, "callspec") and item.callspec.id:
            test_id = item.callspec.id  # e.g., "core:test_author"
            current_module, current_test_name = test_id.split(":", 1)

            match_module = not module_filter or current_module == module_filter
            match_test_name = (
                not test_name_filter or current_test_name == test_name_filter
            )

            if match_module and match_test_name:
                selected_items.append(item)
            else:
                deselected_items.append(item)
        else:
            # If it's not a parametrized test from your action tests, keep it
            selected_items.append(item)

    if deselected_items:
        config.hook.pytest_deselected(items=deselected_items)
        items[:] = selected_items
