# encoding: utf-8
# @Time   : 2021/8/6 15:54
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : class_counter.py
import asyncio

from simple_event_bus import AsyncEventBus, Event

app = AsyncEventBus()


def async_partial(f, *args):
    async def f2(*args2):
        result = f(*args, *args2)
        if asyncio.iscoroutinefunction(f):
            result = await result
        return result

    return f2


class Counter:
    tick_list = []

    def __init__(self):
        app.add_listener("tick", self.tick_collector)
        app.add_listener("teardown", self.teardown)

    async def tick_collector(self, event: Event) -> None:
        print(event.now)
        self.tick_list.append(event)

        if len(self.tick_list) > 5:
            await app.publish_event(Event("clock", message=f"ringing {len(self.tick_list)}"))

        if len(self.tick_list) > 10:
            await app.publish_event("teardown")

    @classmethod
    def teardown(cls, event: Event) -> None:
        event.current_app.close_loop()
        cls.tick_list.clear()

    @staticmethod
    @app.listening("clock")
    async def clock(event: Event) -> None:
        print(event.message)


async def service() -> None:
    Counter()
    await app.run_forever(default_event_type="tick", default_time_interval=0.1)
    print(list(app.get_listener_name_list()))


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(service())
