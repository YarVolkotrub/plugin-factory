# Plugin Contract

A plugin is an object that satisfies the following contract.

## Required methods

A plugin MUST define the following public methods:

- init() -> None  
  Prepares the plugin for execution.  
  Must be called before `start()`.

- start() -> None  
  Starts plugin activity.

- stop() -> None  
  Stops plugin activity and releases resources.

## Required attribute: info

A plugin MUST expose an `info` attribute.

The `info` object MUST contain the following fields:

- name: str  
  Human-readable plugin name.

- state: PluginState  
  Current lifecycle state of the plugin.

- description: str  
  Short description of plugin purpose.

Additional fields are allowed.

## Notes

- `init()` is NOT the same as `__init__()`.
- The contract defines structure, not runtime behavior.
- Lifecycle order is validated separately.
