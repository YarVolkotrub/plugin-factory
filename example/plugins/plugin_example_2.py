from plugin_factory import PluginBase


class ExamplePlugin2(PluginBase):
    """Test plugin 2"""
    NAME = "Example2"
    DESCRIPTION = "Test plugin 2"

    def initialize(self) -> None:
        ...

    def start(self) -> None:
        ...

    def shutdown(self) -> None:
        ...