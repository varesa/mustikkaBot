import logging
import datetime


class _TimeEvent:
    """
    Class to represent a timed action
    """

    type = None # "periodic" or "once"
    """ :type: str"""
    interval = None
    """ :type: datetime.timedelta"""

    next = None
    """ :type: datetime.datetime"""

    action = None
    """ :type: method"""


class TimeManager:
    """
    Class to manage timed events
    """

    log = logging.getLogger("mustikkabot.timemanager")

    time_events = []
    """ :type: list of _TimeEvent"""

    def register_once(self, action, delay):
        """
        :param action: function to be executed
        :type action: function

        :param delay: Delay until action
        :type delay: datetime.timedelta

        Register an event to be executed once
        """
        t = _TimeEvent()

        t.type = "once"
        t.next = datetime.datetime.now() + delay

        t.action = action

        self.time_events.append(t)

    def register_interval(self, action, interval, delay=None):
        """
        :param action: function to be executed
        :type action: function

        :param interval: Delay between actions
        :type interval: datetime.timedelta

        :param delay: Initial delay before first action
        :type delay: datetime.timedelta

        Register an event to be executed at regular intervals
        """
        t = _TimeEvent()
        t.type = "periodic"

        if delay:
            t.next = datetime.datetime.now() + delay
        else:
            t.next = datetime.datetime.now() + interval
        t.interval = interval

        t.action = action

        self.time_events.append(t)

    def unregister(self, action):
        """
        :param action: A timed function to unregister
        :type action: function

        Unregister a timed event to stop it from being executed
        """
        for_removal = []
        for te in self.time_events:
            if te.action == action:
                for_removal.append(te)
        for item in for_removal:
            self.time_events.remove(item)

    def handle_events(self):
        """
        An function to be fired from the main loop at regular intervals
        """
        for_removal = []

        for event in self.time_events:
            if event.next < datetime.datetime.now():
                if event.type == "periodic":
                    event.next += event.interval
                else:
                    for_removal.append(event)
                try:
                    event.action()
                except:
                    self.log.exception("Error happened in a timed event")

        for item in for_removal:
            self.time_events.remove(item)
