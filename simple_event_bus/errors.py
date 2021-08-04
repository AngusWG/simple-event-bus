# encoding: utf-8
# @Time   : 2021/8/3 18:29
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : errors.py


class EventBusBaseError(Exception):
    ...


class NotAsyncFunction(EventBusBaseError, TypeError):
    ...


class ErrorEventType(EventBusBaseError, TypeError):
    ...


class EVENTNameError(EventBusBaseError, NameError):
    ...
