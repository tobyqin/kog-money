from abc import abstractmethod,ABC
from util import tap_only_cords, swipe_cords
import random
import time
from util import check_action
import logging
from match import chose_hero
import os
import json


class Policy(ABC):
    state = None

    @abstractmethod
    def action(self):
        pass


class RandomPlayPolicy(Policy):

    DEFAULT_ACTION = 'random_walk'
    # hero_list = ['bailixuance', 'dunshan', 'laofuzi', 'lianpo',
    #              'caocao','daqiao','mozi','change','miyue','sunbin',]
    hero_list = ['百里玄策', '盾山', '老夫子', '廉颇','曹操', '大乔', '墨子', '嫦娥', '芈月', '孙膑']
    finished = []

    SAVE_PATH= 'finished.json'

    def __init__(self):
        self.state = 0 # started: 1, wait: 0
        self.hero_num = len(self.hero_list)
        self.num_actions = len(tap_only_cords) + len(swipe_cords)
        self.load_finished()

    def save_finished(self):
        with open('finished.json', 'w') as f:
            json.dump(self.finished, f)

    def load_finished(self):
        if os.path.exists(self.SAVE_PATH):
            with open('finished.json', 'r') as f:
                self.finished = json.load(f)

    @staticmethod
    def _random_chose(act):
        i = random.randint(0, len(act) - 1)
        return list(act.keys())[i]

    def _random_hero(self):
        heros = [h for h in self.hero_list if h not in self.finished]
        num = len(heros)
        i = random.randint(0, num - 1)
        self.current_hero = heros[i]
        logging.info("choosing hero: {}".format(self.current_hero))
        return self.current_hero

    def set_finished(self):
        if self.current_hero not in self.finished:
            logging.info('hero {} finished training!!!')
            self.finished.append(self.current_hero)
            self.save_finished()

    def action(self):
        action = check_action()

        # 不在对局中， 没有
        if action not in ['recover', 'pick_hero', 'confirm_hero']:
            time.sleep(1.5)
            return action

        # 确认英雄后，识别到挑选英雄，则略过
        if self.state == 'confirm_hero' and action == 'pick_hero':
            time.sleep(1.5)
            return action

        self.state = action

        if self.state == 'pick_hero':
            if not chose_hero(self._random_hero()):
                chose_hero(self._random_hero())
            return action

        r = random.random()

        if r < 0.5:
            action = self._random_chose(tap_only_cords)
        elif r < 0.7:
            action = self._random_chose(swipe_cords)
        else:
            action = self.DEFAULT_ACTION

        logging.info("ACTION: {}".format(action))
        return action


DEFAULT_POLICY = RandomPlayPolicy()


def get_policy(name='default'):
    return DEFAULT_POLICY
