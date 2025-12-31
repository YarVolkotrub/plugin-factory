from __future__ import annotations

from typing import Mapping, Final
import logging

from plugin_factory.domain.plugin_base import PluginBase
# from .plugin_state import PluginState
# from .state_transitions import StateTransition
# from .interface.transitions_interface import TransitionInterface

logger = logging.getLogger(__name__)

class PluginStateManager:
    """for the future"""
    def __init__(self) -> None:
        ...
    # def __init__(self,
    #              plugins: Mapping[PluginBase],
    #              state_transitions: TransitionInterface,
    #              ) -> None:
    #     logger.debug(f"init {__class__.__name__}")
    #
    #     if not plugins:
    #         raise ValueError("plugins mapping must not be empty")
    #
    #     self.__plugins: Mapping[PluginBase] = plugins
    #
    #     self.__allow_transitions = state_transitions
    #     self.__state_transition = StateTransition(self.__allow_transitions)

        # logger.debug("Initialized %s with %d plugins",
        #             self.__class__.__name__, len(plugins))


    def init_all_plugin(self) -> None:
        logger.debug("Initializing all plugins")

    def start_plugin(self, plugin_name: str) -> None:
        logger.debug("Starting plugin: %s", plugin_name)
        ...

    def stop_plugin(self, plugin_name: str) -> None:
        logger.debug("Stopping plugin: %s", plugin_name)
        ...

    def start_all_plugin(self) ->  None:
        logger.debug("Starting all plugins")
        ...

    def stop_all_plugin(self) -> None:
        logger.debug("Stopping all plugins")
        ...

    def get_plugin_info(self):
        logger.debug("Getting plugin info")


    def get_plugin_states(self):
        logger.debug("Getting plugin states")

    def __change_state(self, new_state, plugin_name) -> None:
        ...
