#!/usr/bin/env python3
"""
Utility script to run pyscaf action tests with filtering.
"""

import os
import subprocess
import sys


def run_tests(module_filter=None, test_filter=None):
    """Run tests with optional filters."""
    # Set environment variables for filtering
    if module_filter:
        os.environ["PYSCAF_TEST_MODULE"] = module_filter
    if test_filter:
        os.environ["PYSCAF_TEST_NAME"] = test_filter

    # Run pytest
    cmd = [sys.executable, "-m", "pytest", "tests/actions/test_actions.py", "-v"]

    result = subprocess.run(cmd)
    return result.returncode


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python run_tests.py                    # Run all tests")
        print("  python run_tests.py core              # Run all core tests")
        print("  python run_tests.py core:test_author  # Run specific test")
        return 1

    arg = sys.argv[1]

    if ":" in arg:
        module_filter, test_filter = arg.split(":", 1)
        return run_tests(module_filter, test_filter)
    else:
        return run_tests(arg, None)


if __name__ == "__main__":
    sys.exit(main())
