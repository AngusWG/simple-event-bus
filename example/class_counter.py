# encoding: utf-8
# @Time   : 2021/8/6 15:54
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : class_counter.py
import asyncio

from simple_event_bus import AsyncEventBus, Event, run_simple_event_source_async

app = AsyncEventBus()


class Counter:
    tick_list = []

    def __init__(self):
        app.add_listener("tick", self.tick_collector)
        app.add_listener("teardown", self.teardown)

    async def tick_collector(self, event: Event) -> None:
        print(event.now)
        self.tick_list.append(event)

        if len(self.tick_list) > 5:
            await app.publish_event(
                Event("clock", message=f"ringing {len(self.tick_list)}")
            )

        if len(self.tick_list) > 10:
            await app.publish_event("teardown")

    @classmethod
    async def teardown(cls, event: Event) -> None:
        await event.current_app.publish_event("close_loop")
        cls.tick_list.clear()

    @staticmethod
    @app.listening("clock")
    async def clock(event: Event) -> None:
        print(event.message)


async def service() -> None:
    Counter()
    await run_simple_event_source_async(app, loop_event="tick", time_interval=0.1)
    print(list(app.get_listener_name_list()))


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(service())
