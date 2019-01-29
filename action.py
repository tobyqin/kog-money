from util import tap_screen, tap_cords, swipe, swipe_cords, tap_only_cords, check_single_action
from abc import ABC, abstractmethod
import time
import logging
import random
from policy import get_policy

action_caches = {}


class Action(ABC):
    def __init__(self, name, cord):
        self.name = name
        self.cord = cord

    @abstractmethod
    def execute(self):
        pass


class SwipeAction(Action):

    def __init__(self, name, cord):
        super(SwipeAction, self).__init__(name, cord)

    def execute(self):
        swipe(*self.cord)


class RandomDirectionSwipeAction(SwipeAction):

    def __init__(self, name, cord):
        super(RandomDirectionSwipeAction, self).__init__(name, cord)
        self.control_center = cord[:2]
        self.length = cord[2]
        self.min_duration = cord[3]
        self.max_duration = cord[4]

    def execute(self):
        x1 = self.control_center[0] + self.length * (random.random() - 0.5)
        y1 = self.control_center[1] + self.length * (random.random() - 0.5)
        duration = random.randint(self.min_duration, self.max_duration)
        logging.debug('walk for {}s to ({},{})'.format(duration, x1, y1))
        self.cord = (*self.control_center, x1, y1, duration)
        super(RandomDirectionSwipeAction, self).execute()


class TapAction(Action):

    def _center_cord(self):
        return (self.cord[0] + self.cord[2]) / 2, (self.cord[1] + self.cord[3]) / 2

    def execute(self):
        tap_screen(*self._center_cord())


class ConfirmAction(TapAction):

    def _center_cord(self):
        return 636, 604


class ContinueAction(TapAction):

    start = time.time()
    count = 0

    def execute(self):
        logging.info("round #{}, 花费时间: {}秒".format(self.count, time.time() - self.start))
        super(ContinueAction, self).execute()
        self.count = self.count + 1
        time.sleep(1)
        self.start = time.time()


class ContinueMatchAction(ContinueAction):

    def __init__(self, name, cord):
        super(ContinueMatchAction, self).__init__(name, cord)
        self.policy = get_policy()

    def execute(self):
        # 第一次点击，并统计时间
        if check_single_action('check_finished'):
            self.policy.set_finished()

        super(ContinueMatchAction, self).execute()

        # 第二次点击
        super(ContinueAction, self).execute()


def get_action_by_name(name):
    try:
        return action_caches[name]
    except KeyError as e:
        if name == 'continue':
            action = ContinueAction(name, tap_cords[name])
        elif name == 'continue_match':
            action = ContinueMatchAction(name, tap_cords[name])
        elif name == 'confirm':
            action = ConfirmAction(name, tap_cords[name])
        elif name in swipe_cords.keys():
            action = RandomDirectionSwipeAction(name, swipe_cords[name])
        elif name in tap_only_cords:
            action = TapAction(name, tap_only_cords[name])
        elif name in tap_cords:
            action = TapAction(name, tap_cords[name])
        else:
            return None
        action_caches[name] = action
        return action
