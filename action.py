from util import tap_screen, boxes
from abc import ABC, abstractmethod
import time
import logging

action_caches = {}


class Action(ABC):
    def __init__(self, name, cord):
        self.name = name
        self.cord = cord

    @abstractmethod
    def execute(self):
        pass


class CenterAction(Action):

    def _center_cord(self):
        return (self.cord[0] + self.cord[2]) / 2, (self.cord[1] + self.cord[3]) / 2

    def execute(self):
        tap_screen(*self._center_cord())


class ContinueAction(CenterAction):

    start = time.time()
    count = 0

    def execute(self):
        logging.info("round #{}, 花费时间: {}秒".format(self.count, time.time() - self.start))
        super(ContinueAction, self).execute()
        self.count = self.count + 1
        time.sleep(1)
        self.start = time.time()


def get_action_by_name(name):
    try:
        return action_caches[name]
    except KeyError as e:
        if name == 'continue':
            action = ContinueAction(name, boxes[name])
        else:
            action = CenterAction(name, boxes[name])
        action_caches[name] = action
        return action
