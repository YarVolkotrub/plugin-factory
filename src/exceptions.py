class PluginError(Exception):
    """Base plugin exception."""


class PluginStorageError(PluginError):
    pass


class PluginImportError(PluginError):
    pass


class PluginValidationError(PluginError):
    pass


class PluginInstantiationError(PluginError):
    pass
