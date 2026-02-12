from plugin_factory import PluginBase




class ExamplePlugin0(PluginBase):
    """Test plugin 0"""
    NAME = "Example0"
    DESCRIPTION = "Test plugin 0"

    def initialize(self) -> None:
        ...

    def start(self) -> None:
        ...

    def shutdown(self) -> None:
        if 1/0:
            raise RuntimeError("Connection failed")
        ...

    def restart(self):
        ...

    def reset(self):
        ...

__plugin__ = ExamplePlugin0