from plugin_factory import PluginBase


class ExamplePlugin2(PluginBase):
    """Test plugin 3"""
    NAME = "Example3"
    DESCRIPTION = "Test plugin 3"

    def initialize(self) -> None:
        ...

    def start(self) -> None:
        ...

    def shutdown(self) -> None:
        ...