# Plugin Factory

## Описание
**Plugin Factory** - это Python‑фреймворк для создания, загрузки и управления жизненным циклом плагинов.

Ключевые цели проекта:
- строгий контракт плагина;
- предсказуемый жизненный цикл (state machine);
- удобный runtime API;

Основной подход к реализации системы плагинов - использование чистого Python без зависимостей от сторонних библиотек.

## Требования

Python 3.11+

## Статус проекта

Проект находится в стадии **pre-prod**.

### Известные ограничения
см. в:
[docs/TODO.md](https://github.com/YarVolkotrub/plugin-factory/blob/main/docs/TODO.md)

### Технические примечания
- `example_main.py` - временный 'main' файл для локального тестирования
- `example/plugins` содержит тестовые плагины для локального тестирования

## Ключевые возможности

- **Плагинная архитектура** с явным контрактом
- **State Machine** для управления жизненным циклом плагинов
- **Factory‑подход** для централизованного создания плагинов
- **Runtime API** для управления жизненным циклом плагинов

## Структура проекта
Проект организован по слоям (contracts → core → infrastructure → runtime):
```
plugin-factory/
├── docs/
│   └── plugin_system_architecture.md   # Описание архитектуры проекта
├── example/
│   ├── example_main.py                 # Пример использования
│   └── plugins/                        # Примеры плагинов
├── src/
│   └── plugin_factory/
│       ├── contracts/                  # Контракты и интерфейсы
│       ├── core/                       # Базовая логика
│       ├── infrastructure/             # State machine и инфраструктура
│       └── runtime/                    # Runtime API
├── tests/                              # Тесты
├── pyproject.toml                      # Конфигурация проекта
└── README.md
```

## Контракт плагина, жизненный цикл и основные требования к реализации и изменению

Подробное описание см. в:
[docs/plugin_system_architecture.md](https://github.com/YarVolkotrub/plugin-factory/blob/main/docs/plugin_system_architecture.md)

___
