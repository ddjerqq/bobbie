from __future__ import annotations


class Event(object):
    def __init__(self) -> None:
        self.__event_handlers = []

    def __iadd__(self, handler: callable) -> Event:
        self.__event_handlers.append(handler)
        return self

    def __isub__(self, handler: callable) -> Event:
        self.__event_handlers.remove(handler)
        return self

    def __call__(self, *args, **kwargs) -> None:
        for handler in self.__event_handlers:
            try:
                handler(*args, **kwargs)
            except Exception as e:
                print(type(e))
                print(e)
                print(e.__cause__)
                print(e.__context__)
            finally:
                continue


class Server:
    def __init__(self, *args, **kwargs) -> None:
        self.on_message = Event()

    def get_message(self, msg):
        print(msg)
        self.on_message(msg)


s = Server()
s.on_message = lambda: print("logged new message to the ughh thing! ;) u get the idea")

s.get_message("hello im a message")


class Lock(object):
    def __init__(self, *args, **kwargs) -> None:
        self.on_break: Event = Event()

    def break_lock(self):
        self.on_break()


lock = Lock()


def call_police():
    print("police called")


def call_owner():
    print("owner called")


def call_alarm():
    print("alarm called")


lock.on_break += call_police
lock.on_break += call_owner
lock.on_break += call_alarm


lock.break_lock()
