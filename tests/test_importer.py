import types
import pytest

from src.loader.importer import ModuleImporter
from src.exceptions import PluginImportError


def test_importer_imports_existing_module():
    importer = ModuleImporter()
    module = importer.import_module("sys")

    assert module is not None


def test_importer_raises_on_invalid_module():
    importer = ModuleImporter()

    with pytest.raises(PluginImportError):
        importer.import_module("non_existing_module_xyz")
