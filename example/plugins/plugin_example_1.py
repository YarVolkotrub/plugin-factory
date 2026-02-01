from plugin_factory import PluginBase


class ExamplePlugin1(PluginBase):
    """Test plugin 1'"""
    NAME = "Example1"
    DESCRIPTION = "Test plugin 1"

    def initialize(self) -> None:
        ...

    def start(self) -> None:
        ...

    def shutdown(self) -> None:
        ...
