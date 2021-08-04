# encoding: utf-8
# @Time   : 2021/8/4 14:50
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : counter.py
import asyncio

from simple_event_bus import AsyncEventBus, Event

app = AsyncEventBus()
tick_list = []


@app.listening("tick")
async def tick_collector(event: Event) -> None:
    print(event.now)
    tick_list.append(event)

    if len(tick_list) > 5:
        await app.publish_event(Event("clock", message=f"ringing {len(tick_list)}"))

    if len(tick_list) > 10:
        await app.publish_event("teardown")


@app.listening("clock")
async def clock(event: Event) -> None:
    print(event.message)


@app.listening("teardown")
def teardown(event: Event) -> None:
    event.current_app.close_loop()


async def service() -> None:
    await app.run_forever(default_event_type="tick", default_time_interval=0.1)
    print(list(app.get_listener_name_list()))


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(service())
