import pytest

from src.loader.factory import PluginFactory
from src.interfaces.plugin import PluginBase
from tests.plugins.plugin_test_plugi import TestPlugin


class BadPluginBase(PluginBase):
    name = "bad"

    def __init__(self):
        raise RuntimeError("boom")

    def start(self): ...
    def stop(self): ...


def test_factory_creates_plugin():
    factory = PluginFactory()
    plugin = factory.create(TestPlugin)

    assert plugin.name == "test"


def test_factory_raises_on_error():
    factory = PluginFactory()

    with pytest.raises(Exception):
        factory.create(BadPluginBase)
