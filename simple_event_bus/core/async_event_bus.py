# encoding: utf-8
# @Time   : 2021/8/4 12:04
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : ${FILE_NAME}
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
        default_event_name: EVENT = EVENT("HeartBeat"),
        default_time_interval: int = 1,
    ) -> None:
        self._loop_enable = True
        self._default_event_name = default_event_name
        self._time_interval = default_time_interval

        while self._loop_enable:
            await self.publish_event(
                Event(self._default_event_name, now=datetime.datetime.now())
            )
            await asyncio.sleep(self._time_interval)
        return
