import sys
from pathlib import Path

from src.loader.loader import PluginLoader
from src.loader.importer import ModuleImporter
from src.loader.factory import PluginFactory
from src.loader.class_finder import PluginClassFinder
from src.Implementations.local_storage import LocalStorage
from src.Implementations.local_plugin_finder import LocalPluginFinderBase
from src.validation.plugin_validator import PluginValidator


def test_loader_loads_plugins(tmp_path: Path):
    project_root = Path(__file__).parents[1]

    sys.path.insert(0, str(project_root))
    sys.path.insert(0, str(tmp_path))

    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir()
    (plugins_dir / "__init__.py").write_text("")

    plugin_file = plugins_dir / "plugin_test.py"
    plugin_file.write_text(
        "from src.interfaces.IPlugin import IPlugin\n"
        "class TestPlugin(IPlugin):\n"
        "    name = 'test'\n"
        "    def start(self): pass\n"
        "    def stop(self): pass\n"
    )

    storage = LocalStorage(plugins_dir, pattern="plugin*.py")
    finder = LocalPluginFinderBase(root_package="plugins")

    loader = PluginLoader(
        storage=storage,
        finder=finder,
        validator=PluginValidator(),
        importer=ModuleImporter(),
        class_finder=PluginClassFinder(),
        factory=PluginFactory(),
    )

    plugins = loader.load()

    assert "test" in plugins


