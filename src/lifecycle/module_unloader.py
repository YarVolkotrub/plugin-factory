import sys


class ModuleUnloader:
    def unload_plugin(self, plugin) -> None:
        if plugin not in sys.path:
            raise ...

        try:
            del sys.modules[plugin]
        except:
            ...