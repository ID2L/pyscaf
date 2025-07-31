"""
Test suite for pyscaf actions using YAML configuration files.
"""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List

import pytest
import yaml


class ActionTestRunner:
    """Runner for testing pyscaf actions using YAML configuration files."""

    def __init__(self, test_file_path: Path):
        self.test_file_path = test_file_path
        self.config = self._load_config()
        self.temp_dir = None

    def _load_config(self) -> Dict[str, Any]:
        """Load and validate the YAML configuration file."""
        with open(self.test_file_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        # Validate required fields
        required_fields = ["checks"]
        for field in required_fields:
            if field not in config:
                raise ValueError(
                    f"Missing required field '{field}' in {self.test_file_path}"
                )

        return config

    def _create_temp_directory(self) -> Path:
        """Create a temporary directory for testing."""
        self.temp_dir = Path(tempfile.mkdtemp())
        return self.temp_dir

    def _build_cli_command(self) -> List[str]:
        """Build the CLI command with arguments from config."""
        cmd = ["pyscaf", "init", "tmp_project", "--no-install"]

        # Add CLI arguments if they exist and are not empty
        cli_args = self.config.get("cli_arguments", {})
        if cli_args:
            for key, value in cli_args.items():
                if isinstance(value, bool):
                    if value:
                        cmd.append(f"--{key}")
                    else:
                        cmd.append(f"--no-{key}")
                else:
                    cmd.append(f"--{key}")
                    cmd.append(str(value))

        return cmd

    def _execute_command(
        self, cmd: List[str], cwd: Path
    ) -> subprocess.CompletedProcess:
        """Execute the CLI command in the specified directory."""
        try:
            result = subprocess.run(
                cmd, cwd=cwd, capture_output=True, text=True, timeout=60
            )
            return result
        except subprocess.TimeoutExpired:
            raise TimeoutError(f"Command timed out: {' '.join(cmd)}")

    def _check_file_exists(self, file_path: str) -> bool:
        """Check if a file exists in the temporary directory."""
        if not self.temp_dir:
            return False
        full_path = self.temp_dir / file_path
        return full_path.exists()

    def _check_file_contains(self, file_path: str, content: str) -> bool:
        """Check if a file contains the specified content."""
        if not self.temp_dir:
            return False
        full_path = self.temp_dir / file_path
        if not full_path.exists():
            return False

        try:
            with open(full_path, "r", encoding="utf-8") as f:
                file_content = f.read()
            return content in file_content
        except Exception:
            return False

    def _execute_custom_check(self, function_path: str) -> bool:
        """Execute a custom check function."""
        try:
            # Import the function dynamically
            module_path, function_name = function_path.rsplit(":", 1)
            module = __import__(module_path, fromlist=[function_name])
            function = getattr(module, function_name)

            # Execute the function with temp_dir as argument
            return function(self.temp_dir)
        except Exception as e:
            print(f"Error executing custom check {function_path}: {e}")
            return False

    def _run_checks(self) -> List[Dict[str, Any]]:
        """Run all checks and return results."""
        results = []

        for check in self.config["checks"]:
            check_name = check["name"]
            check_type = check["type"]
            file_path = check.get("file_path", "")
            content = check.get("content", "")
            function_path = check.get("function_path", "")

            result = {
                "name": check_name,
                "type": check_type,
                "file_path": file_path,
                "success": False,
                "error": None,
            }

            try:
                if check_type == "exist":
                    result["success"] = self._check_file_exists(file_path)
                elif check_type == "not_exist":
                    result["success"] = not self._check_file_exists(file_path)
                elif check_type == "contains":
                    result["success"] = self._check_file_contains(file_path, content)
                elif check_type == "not_contains":
                    result["success"] = not self._check_file_contains(
                        file_path, content
                    )
                elif check_type == "custom":
                    result["success"] = self._execute_custom_check(function_path)
                else:
                    result["error"] = f"Unknown check type: {check_type}"

            except Exception as e:
                result["error"] = str(e)

            results.append(result)

        return results

    def run_test(self) -> Dict[str, Any]:
        """Run the complete test for this configuration."""
        # Create temporary directory
        temp_dir = self._create_temp_directory()

        try:
            # Build and execute command
            cmd = self._build_cli_command()
            result = self._execute_command(cmd, temp_dir)

            # Run checks
            check_results = self._run_checks()

            return {
                "test_file": str(self.test_file_path),
                "command": " ".join(cmd),
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "check_results": check_results,
                "all_checks_passed": all(check["success"] for check in check_results),
            }

        finally:
            # Clean up temporary directory
            if self.temp_dir and self.temp_dir.exists():
                import shutil

                shutil.rmtree(self.temp_dir)


def discover_test_files(
    module_filter: str | None = None, test_filter: str | None = None
) -> List[tuple[Path, str]]:
    """Discover all YAML test files in the tests/actions directory."""
    tests_dir = Path(__file__).parent
    test_files = []

    for yaml_file in tests_dir.rglob("*.yaml"):
        # Extract module name from path (e.g., "core" from "tests/actions/core/test1.yaml")
        relative_path = yaml_file.relative_to(tests_dir)
        module_name = relative_path.parts[0] if len(relative_path.parts) > 1 else "root"
        test_name = yaml_file.stem

        # Apply filters
        if module_filter and module_name != module_filter:
            continue
        if test_filter and test_name != test_filter:
            continue

        # Create a descriptive test name
        test_id = f"{module_name}:{test_name}"
        test_files.append((yaml_file, test_id))

    return test_files


def get_test_files_from_args():
    """Get test files based on environment variables."""
    # Check for environment variables
    module_filter = os.environ.get("PYSCAF_TEST_MODULE")
    test_filter = os.environ.get("PYSCAF_TEST_NAME")

    if module_filter or test_filter:
        return discover_test_files(module_filter, test_filter)

    # Default: all tests
    return discover_test_files()


# Use a simpler approach that works better with pytest
test_files_data = get_test_files_from_args()
test_ids = [test_id for _, test_id in test_files_data]


@pytest.mark.parametrize("test_file,test_id", test_files_data, ids=test_ids)
def test_action(test_file: Path, test_id: str):
    """Test an action using its YAML configuration file."""
    runner = ActionTestRunner(test_file)
    result = runner.run_test()

    # Assert that all checks passed
    assert result["all_checks_passed"], (
        f"Test failed for {test_id}:\n"
        f"Command: {result['command']}\n"
        f"Return code: {result['return_code']}\n"
        f"Check results: {result['check_results']}\n"
        f"stdout: {result['stdout']}\n"
        f"stderr: {result['stderr']}"
    )

    # Also assert that the command executed successfully
    assert result["return_code"] == 0, (
        f"Command failed with return code {result['return_code']}:\n"
        f"Command: {result['command']}\n"
        f"stdout: {result['stdout']}\n"
        f"stderr: {result['stderr']}"
    )
