from __future__ import annotations
from importlib import import_module
from types import ModuleType

from ..exceptions import PluginImportError


class ModuleImporter:
    def import_module(self, import_path: str) -> ModuleType | None:
        try:
            return import_module(import_path)
        except Exception as exc:
            raise PluginImportError(import_path) from exc
