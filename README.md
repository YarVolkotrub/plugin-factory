# Plugin Factory

Plugin Factory is a lightweight and extensible plugin system for Python applications. It allows you to dynamically discover, load, and manage plugins without modifying the core application.

---

## 🚀 Features
- **Dynamic plugin discovery** via directory scanning
- **Automatic module importing**
- **Strict plugin validation** using the `IPlugin` interface
- **Safe class detection** (no use of `__subclasses__()`, only module-local classes)
- **Plugin lifecycle management**: start, stop, start_all, stop_all
- **Clean architecture**, simple to extend

---

## 📁 Project Structure
```
project/
│ plugin_loader.py      # Plugin discovery & initialization
│ plugin_manager.py     # Plugin lifecycle management
│ IPlugin.py            # Abstract plugin interface
│ __init__.py           # Shared constants
│
└── plugins/            # Directory containing user plugins
```

---

## 🧩 IPlugin Interface
All plugins must implement the following interface:

```python
from abc import ABC, abstractmethod

class IPlugin(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def status(self) -> str: ...

    @abstractmethod
    def start(self) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...
```

### Plugin requirements:
- `name` — unique identifier
- `status` — human-readable plugin state
- `start()` — run startup logic
- `stop()` — run cleanup logic

---

## 🔍 PluginLoader
Used to discover and load plugins dynamically.

### Usage:
```python
from plugin_loader import PluginLoader
loader = PluginLoader()
plugins = loader.load()
```

### How it works:
1. Scans `plugins/` directory for subfolders
2. Inside each folder, looks for modules matching:
   ```
   plugin_*.py
   ```
3. Imports modules dynamically
4. Detects valid plugin classes based on:
   - Inheritance from `IPlugin`
   - Not abstract
   - Defined inside the module
5. Instantiates plugin objects

---

## ⚙️ PluginManager
Manages lifecycle of plugins.

### Usage:
```python
from plugin_manager import PluginManager
manager = PluginManager(plugins)

manager.start("logger")
manager.stop("logger")

manager.start_all()
manager.stop_all()

manager.get_status()
```

### Provides:
- Start/stop individual plugins
- Start/stop all plugins
- Query status of all plugins

---

## 📝 Example Plugin
File:
```
plugins/logger/plugin_logger.py
```

```python
from IPlugin import IPlugin

class LoggerPlugin(IPlugin):
    @property
    def name(self) -> str:
        return "logger"

    @property
    def status(self) -> str:
        return "ready"

    def start(self) -> None:
        print("Logger started")

    def stop(self) -> None:
        print("Logger stopped")
```

---

## 🧱 Extending the Framework
You can extend Plugin Factory by adding:
- Plugin metadata
- Plugin categories
- Hot-reload system
- Dependency resolution
- Versioning support

---

## 📄 License
MIT License

---

## 💬 Author
Plugin Factory — created by Yaroslav Volkotrub

---
