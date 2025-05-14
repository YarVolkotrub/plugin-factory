from os import path
from glob import glob
from importlib import import_module

from .basePlugin import BasePlugin

__all__ = [path, glob, import_module, BasePlugin]

Plugin_Template: str = '/*/plugin*.py'
Dir_With_Plugins: str = 'plugins'
