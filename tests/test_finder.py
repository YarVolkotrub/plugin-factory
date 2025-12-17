from pathlib import Path

from src.Implementations.local_plugin_finder import LocalPluginFinderBase


def test_finder_builds_import_paths():
    files = [
        Path("/project/src/plugins/logger/plugin_logger.py")
    ]

    finder = LocalPluginFinderBase(root_package="plugins")
    result = finder.find(files)

    assert result == ["plugins.logger.plugin_logger"]
