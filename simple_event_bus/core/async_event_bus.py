# encoding: utf-8
# @Time   : 2021/8/4 12:04
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : async_event_bus.py
import asyncio
import datetime
import inspect
from typing import Union

from simple_event_bus.core.event import EVENT, EVENT_TYPE, Event
from simple_event_bus.core.event_bus import EventBus


class AsyncEventBus(EventBus):
    async def publish_event(self, event: Union[Event, EVENT_TYPE]) -> None:
        event = self._event_format(event)
        self.logger.debug(f"Get {event}")
        for listener in self._listeners[event.event_type]:
            if inspect.iscoroutinefunction(listener):
                res = await listener(event)
            else:
                res = listener(event)
            if res:
                # if listener return true. will break the loop
                self.logger.debug(f"{listener.__name__} break the loop")
                break

    async def run_forever(
        self,
        default_event_type: EVENT_TYPE = EVENT("HeartBeat"),
        default_time_interval: Union[int, float] = 1,
    ) -> None:
        self._loop_enable = True
        self._default_event_type = self._event_type_format(default_event_type)
        self._time_interval = default_time_interval

        while self._loop_enable:
            await self.publish_event(
                Event(self._default_event_type, now=datetime.datetime.now())
            )
            await asyncio.sleep(self._time_interval)
        return
