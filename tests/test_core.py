# encoding: utf-8
# @Time   : 2021/8/4 11:09
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : test_core.py
import pytest

from simple_event_bus import MultiParamFunctionError


class TestCore:
    def test_event(self):
        from simple_event_bus.core import EVENT
        from simple_event_bus.errors import EVENTNameError

        with pytest.raises(EVENTNameError):
            EVENT("a event")

    def test_basic_event_bus(self):
        from simple_event_bus.core import EVENT, Event, EventBus

        app = EventBus()
        event_list = []

        @app.listening("HeartBeat")
        def count(event: Event):
            event_list.append(event)
            if len(event_list) > 5:
                app.publish_event(Event(EVENT("close_loop")))
            return True

        app.run_forever()
        assert len(event_list) > 5

        with pytest.raises(MultiParamFunctionError):

            @app.listening("HeartBeat")
            def error_func():
                print("this is a error function")
                return

    @pytest.mark.asyncio
    async def test_async_event_bus(self):
        from simple_event_bus.core import EVENT, AsyncEventBus, Event

        app = AsyncEventBus()

        event_list = []
        async_event_list = []

        @app.listening("HeartBeat")
        def count(event: Event):
            event_list.append(event)
            if len(event_list) <= 5:
                return True

        @app.listening(EVENT("HeartBeat"))
        async def async_count(event: Event):
            async_event_list.append(event)
            if len(async_event_list) == 5:
                await app.publish_event("close_loop")

        await app.run_forever()
        assert len(event_list) == 10
        assert len(async_event_list) == 5
        assert "async_count" in app.get_listener_name_list("HeartBeat")
