import tempfile
from pathlib import Path

import tomli

from pyscaf.tools.toml_merge import merge_toml_files


def write_toml(path, data):
    import tomli_w

    with open(path, "wb") as f:
        tomli_w.dump(data, f)


def read_toml(path):
    with open(path, "rb") as f:
        return tomli.load(f)


def test_simple_merge():
    with tempfile.TemporaryDirectory() as tmpdir:
        src = Path(tmpdir) / "src.toml"
        dst = Path(tmpdir) / "dst.toml"
        write_toml(src, {"a": 1, "b": 2})
        write_toml(dst, {"b": 3, "c": 4})
        merge_toml_files(src, dst)
        result = read_toml(dst)
        assert result == {"a": 1, "b": 2, "c": 4}


def test_nested_merge():
    with tempfile.TemporaryDirectory() as tmpdir:
        src = Path(tmpdir) / "src.toml"
        dst = Path(tmpdir) / "dst.toml"
        write_toml(src, {"tool": {"pyscaf": {"x": 1, "y": {"z": 2}}}})
        write_toml(dst, {"tool": {"pyscaf": {"y": {"w": 3}, "other": 5}}})
        merge_toml_files(src, dst)
        result = read_toml(dst)
        assert result["tool"]["pyscaf"]["x"] == 1
        assert result["tool"]["pyscaf"]["y"] == {"z": 2, "w": 3}
        assert result["tool"]["pyscaf"]["other"] == 5


def test_list_merge():
    with tempfile.TemporaryDirectory() as tmpdir:
        src = Path(tmpdir) / "src.toml"
        dst = Path(tmpdir) / "dst.toml"
        write_toml(src, {"a": [1, 2, 3]})
        write_toml(dst, {"a": [3, 4]})
        merge_toml_files(src, dst)
        result = read_toml(dst)
        assert sorted(result["a"]) == [1, 2, 3, 4]


def test_overwrite():
    with tempfile.TemporaryDirectory() as tmpdir:
        src = Path(tmpdir) / "src.toml"
        dst = Path(tmpdir) / "dst.toml"
        write_toml(src, {"a": "new", "b": 2})
        write_toml(dst, {"a": "old", "b": 1, "c": 3})
        merge_toml_files(src, dst)
        result = read_toml(dst)
        assert result["a"] == "new"
        assert result["b"] == 2
        assert result["c"] == 3


def test_no_overwrite_unrelated():
    with tempfile.TemporaryDirectory() as tmpdir:
        src = Path(tmpdir) / "src.toml"
        dst = Path(tmpdir) / "dst.toml"
        write_toml(src, {"x": 1})
        write_toml(dst, {"y": 2})
        merge_toml_files(src, dst)
        result = read_toml(dst)
        assert result["x"] == 1
        assert result["y"] == 2
