# encoding: utf-8
# @Time   : 2021/8/4 14:50
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : counter_sync.py
import datetime
import time

from simple_event_bus import Event, EventBus

app = EventBus()
tick_list = []


@app.listening("HeartBeat")
def tick_collector(event: Event) -> None:
    print(event.now)
    tick_list.append(event)
    if len(tick_list) > 5:
        app.publish_event("close_loop")


def event_source_maker() -> None:
    for i in range(10):
        app.publish_event(Event("HeartBeat", now=datetime.datetime.now()))
        time.sleep(0.1)


if __name__ == "__main__":
    event_source_maker()
