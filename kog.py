# -*- coding: utf-8 -*-

import logging
import os
from baseline import check_action, save_crop, convert_cord


# 刷金币次数
repeat_times = 60

# 日志输出
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)


def tap_screen(x, y):
    """calculate real x, y according to device resolution."""
    real_x, real_y = convert_cord(x, y)
    cmd = 'adb shell input tap {} {}'.format(real_x, real_y)
    logging.debug(cmd)
    os.system(cmd)


def take_action(action):
    if not action:
        return
    if action == 'restart':
        tap_screen(1877, 993)
    elif action == 'start':
        tap_screen(1600, 888)
    elif action in ['skip0', 'skip1']:
        tap_screen(2080, 44)
    elif action == 'continue':
        tap_screen(1074, 971)
    elif action == 'exit':
        tap_screen(1950, 100)


if __name__ == '__main__':
    # save_crop()
    while True:
        action = check_action()
        take_action(action)
