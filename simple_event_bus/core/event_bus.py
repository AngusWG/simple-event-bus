# encoding: utf-8
# @Time   : 2021/8/4 12:04
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : event_bus.py
import datetime
import inspect
import logging
import time
from collections import defaultdict
from functools import lru_cache
from typing import Callable, Dict, List, Union

from simple_event_bus.core.event import EVENT, EVENT_TYPE, Event
from simple_event_bus.errors import MultiParamFunctionError


class EventBus(object):
    def __init__(self):
        self._default_event_type: EVENT = EVENT("HeartBeat")
        self._time_interval: int = 0
        self._loop_enable: bool = False
        self._listeners: Dict[str, List[Callable]] = defaultdict(list)

        self.add_listener(EVENT("close_loop"), self.close_loop)
        self.logger = logging.getLogger("simple_event_bus")

    @staticmethod
    @lru_cache()
    def _event_type_format(event_type: EVENT_TYPE) -> EVENT:
        if isinstance(event_type, str):
            return EVENT(event_type)

    @lru_cache()
    def _event_format(self, event: Union[Event, EVENT_TYPE]) -> Event:
        if isinstance(event, str):
            event: EVENT = EVENT(event)
        if isinstance(event, EVENT):
            event: Event = Event(event)
        if event.current_app is None:
            event.current_app = self
        return event

    def add_listener(self, event_type: EVENT_TYPE, listener: Callable) -> None:
        # args check
        event_type = self._event_type_format(event_type)
        signature = inspect.signature(listener)
        if len(signature.parameters) != 1:
            raise MultiParamFunctionError(MultiParamFunctionError.__doc__)
        # append
        self._listeners[event_type].append(listener)

    def listening(self, event_type: EVENT_TYPE) -> Callable:
        """add listener by wrapper"""
        event_type = self._event_type_format(event_type)

        def wrapper(listener: Callable) -> Callable:
            self.add_listener(event_type, listener)
            return listener

        return wrapper

    def publish_event(self, event: Event) -> None:
        self._event_format(event)
        self.logger.debug(f"Get {event}")
        for listener in self._listeners[event.event_type]:
            if listener(event):
                # if listener return true. will break the loop
                self.logger.debug(f"{listener.__name__} break the loop")
                break

    def get_listener_name_list(self, event_type: EVENT_TYPE = None) -> List[str]:
        if event_type is None:
            for listener_list in self._listeners.values():
                for listener in listener_list:
                    yield listener.__name__

        event_type = self._event_type_format(event_type)
        for listener in self._listeners[event_type]:
            yield listener.__name__

    def run_forever(
        self,
        default_event_type: EVENT_TYPE = EVENT("HeartBeat"),
        default_time_interval: Union[int, float] = 1,
    ) -> None:
        self._loop_enable = True
        self._default_event_type = self._event_type_format(default_event_type)
        self._time_interval = default_time_interval

        while self._loop_enable:
            self.publish_event(
                Event(self._default_event_type, now=datetime.datetime.now())
            )
            time.sleep(self._time_interval)
        return

    def close_loop(self, _: Event = None) -> None:
        """关闭循环"""
        self._loop_enable = False
