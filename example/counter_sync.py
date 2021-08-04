# encoding: utf-8
# @Time   : 2021/8/4 14:50
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : counter_sync.py

from simple_event_bus import Event, EventBus

app = EventBus()
tick_list = []


@app.listening("HeartBeat")
def tick_collector(event: Event) -> None:
    print(event.now)
    tick_list.append(event)
    if len(tick_list) > 5:
        app.publish_event("close_loop")


app.run_forever(default_time_interval=0.1)
