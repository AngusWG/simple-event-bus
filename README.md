# simple-event-bus

--- 

a simple python event bus

## Install:

``` bash
pip install simple_event_bus
```

## Example:

```bash
import asyncio

from simple_event_bus import AsyncEventBus, Event, run_simple_event_source_async

app = AsyncEventBus()
tick_list = []


@app.listening("HeartBeat")
async def tick_collector(event: Event) -> None:
    print(event.now)
    tick_list.append(event)
    if len(tick_list) > 5:
        await app.publish_event("close_loop")


asyncio.get_event_loop().run_until_complete(run_simple_event_source_async(app))
```

## Features

* EventBus
* AsyncEventBus
* EventBus.run_forever function
* EventBus.publish_event accept Event , EVENT_TYPE and str.
* Event can get current_app
* listening function args check
* add remove method
* allow no param method to listening
* [x] Independent event sources
* [ ] add before event listener and after event listener

---

* [Black formatter](https://github.com/psf/black)

> This project use black, please set `Continuation indent` = 4  
> Pycharm - File - Settings - Editor - Code Style - Python - Tabs and Indents

* [Flake8 lint](https://github.com/PyCQA/flake8)

> Use flake8 to check your code style.

* This project is made by [AngusWG/cookiecutter-py-package](https://github.com/AngusWG/cookiecutter-py-package.git)
