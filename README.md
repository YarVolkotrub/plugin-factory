# Plugin Factory

**Plugin Factory** - это Python-фреймворк для загрузки, валидации и управления жизненным циклом плагинов с чётко определённым контрактом и строгим lifecycle.

Проект ориентирован на:
- модульные системы;
- расширяемые приложения;
- плагины с управляемым состоянием;
- production-использование.

## Требования

Python 3.11+

Без внешних зависимостей (на текущем этапе)

## Статус проекта
***MVP***, ниже описано текущая или ближайшая стадия разработки

⚠️example_main.py - временный файл, используется только для локального тестирования.

⚠️Каталог plugins/ содержит тестовые плагины, включая намеренно некорректные.

## Ключевые возможности

- 🔌 Плагинная архитектура
- 📜 Строгий контракт плагина
- 🔁 Управляемый lifecycle (state-machine)
- 🧱 Явное разделение ответственности

## Контракт плагина

Каждый плагин обязан наследоваться от "PluginBase" и реализует:
```py
    @property
    @abstractmethod
    def info(self) -> PluginInfo:
        """Get info about the plugin."""

    @info.setter
    @abstractmethod
    def info(self, value: PluginInfo) -> None:
        """Set info about the plugin."""

    @abstractmethod
    def init(self) -> None:
        """Initialize the plugin."""

    @abstractmethod
    def start(self) -> None:
        """Start the plugin."""

    @abstractmethod
    def stop(self) -> None:
        """Stop the plugin."""
```

И содержать объект PluginInfo с полями:
```py
class PluginInfo:
    name: str
    state: PluginState = field(default=PluginState.CREATED)
    description: Optional[str] = field(default=None, compare=False)
    error: Optional[Exception] = field(default=None, compare=False, repr=False)
```

## lifecycle (state-machine)
Допустимые состояния и действия

    PluginState.CREATED - "Plugin created but not initialized",
    PluginState.INITIALIZED - "Plugin initialized and ready to start",
    PluginState.STARTED - "Plugin is running",
    PluginState.STOPPED - "Plugin stopped",
    PluginState.FAILED - "Plugin failed with error"

    ACTION_DESCRIPTIONS:
    PluginAction.INIT - "Initialize plugin",
    PluginAction.START - "Start plugin execution",
    PluginAction.STOP - "Stop plugin execution"
    PluginAction.FAIL - "Plugin failed with error",
    PluginAction.RESET - "Reset plugin state",
    PluginAction.RESTART - "Restart plugin execution",


## Планы развития

- Доработать lifecycle (state-machine)
- Доработать валидацию
- ???Расширить набор состояний???
- Добавить централизованное логирование
- Ввести иерархию ошибок
- Переработать manager
- Тесты
- Docstring
- Документация
- Расширить источники загрузки плагинов:
  - Добавить загрузку/выгрузку плагинов на "горячую"
  - Добавить поддержка плагинов из формата json/yaml
- async плагины
- callback плагины
- CLI-инструменты
- Dashboard мониторинг