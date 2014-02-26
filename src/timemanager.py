import re
import logging
import datetime

class _TimeEvent:
    type = None # "periodic" or "once"
    interval = None

    next = None

    action = None


class TimeManager:

    log = logging.getLogger("mustikkabot.timemanager")

    time_events = []

    def register_once(self, delay):
        t = _TimeEvent()
        t.type = "once"
        t.next = datetime.datetime.now() + delay

        self.time_events.append(t)

    def register_interval(self, interval, delay=None):
        t = _TimeEvent()
        t.type = "interval"
        if delay:
            t.next = datetime.datetime.now() + delay
        else:
            t.next = datetime.datetime.now() + interval
        t.interval = interval

        self.time_events.append(t)

    def handle_events(self):
        for event in self.time_events:
            if event.next < datetime.datetime.now():
                if event.type == "periodic":
                    event.next += event.interval
                else:
                    self.time_events.remove(event)
                try:
                    event.action()
                except:
                    self.log.error("Error happened in a timed event")
