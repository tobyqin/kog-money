import json
import logging
import os
import random
import time
from abc import abstractmethod, ABC

from match import chose_hero
from util import check_action
from util import tap_only_cords, swipe_cords, stop_game


class Policy(ABC):
    state = None

    @abstractmethod
    def action(self):
        pass


class RandomPlayPolicy(Policy):

    DEFAULT_ACTION = 'random_walk'
    hero_list = ['bailixuance', 'dunshan', 'laofuzi', 'lianpo',
                 'caocao','daqiao','mozi','change','miyue','sunbin',]
    finished = []

    SAVE_PATH = 'finished.json'
    HERO_PATH = 'hero.json'
    current_hero = None

    def __init__(self):
        self.state = 0 # started: 1, wait: 0
        self.hero_num = len(self.hero_list)
        self.num_actions = len(tap_only_cords) + len(swipe_cords)
        self.load_finished()
        self.load_hero()

    def save_finished(self):
        with open(self.SAVE_PATH, 'w') as f:
            json.dump(self.finished, f)

    def load_finished(self):
        if os.path.exists(self.SAVE_PATH):
            with open(self.SAVE_PATH, 'r') as f:
                self.finished = json.load(f)

    def load_hero(self):
        if os.path.exists(self.HERO_PATH):
            with open(self.HERO_PATH, 'r') as f:
                self.hero_list = json.load(f)

    @staticmethod
    def _random_chose(act):
        i = random.randint(0, len(act) - 1)
        return list(act.keys())[i]

    def _random_hero(self):
        heros = [h for h in self.hero_list if h not in self.finished]
        num = len(heros)
        if num == 0:
            logging.info("所有英雄已经刷完，退出游戏")
            stop_game()
            exit(0)
        i = random.randint(0, num - 1)
        hero = heros[i]
        logging.info("choosing hero: {}".format(hero))
        return hero

    def set_finished(self):
        if not self.current_hero:
            logging.warning("hero finished, no hero saved!")
        if self.current_hero and self.current_hero not in self.finished:
            logging.info('hero {} finished training!!!'.format(self.current_hero))
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
            return None

        logging.debug("old state:{}, new state:{}".format(self.state, action))
        self.state = action

        if self.state == 'confirm_hero':
            return action

        if self.state == 'pick_hero':
            hero = self._random_hero()
            if not chose_hero(hero):
                logging.debug('find hero {} failed, retry'.format(hero))
                hero = self._random_hero()
                chose_hero(hero, reverse=True)
                logging.debug('try to find hero {}'.format(hero))

            self.current_hero = hero
            time.sleep(1)
            return action

        r = random.random()

        if r < 0.5:
            action = self._random_chose(tap_only_cords)
        elif r < 0.7:
            action = self._random_chose(swipe_cords)
        else:
            action = self.DEFAULT_ACTION

        logging.debug("ACTION: {}".format(action))
        return action


DEFAULT_POLICY = RandomPlayPolicy()


def get_policy(name='default'):
    return DEFAULT_POLICY
