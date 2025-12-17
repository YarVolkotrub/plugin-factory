from pathlib import Path
import pytest

from src.Implementations.local_storage import LocalStorage
from src.exceptions import PluginStorageError


def test_storage_returns_plugin_files(tmp_path: Path):
    plugin_dir = tmp_path / "plugins"
    plugin_dir.mkdir()

    file = plugin_dir / "plugin_test.py"
    file.write_text("")

    storage = LocalStorage(plugin_dir)
    files = storage.get()

    assert file in files


def test_storage_raises_if_dir_missing(tmp_path: Path):
    storage = LocalStorage(tmp_path / "missing")

    with pytest.raises(PluginStorageError):
        storage.get()
