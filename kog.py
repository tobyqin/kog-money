# -*- coding: utf-8 -*-

import timeit
import logging
import os
from time import sleep
from PIL import Image
from baseline import check_action

# 屏幕分辨率
device_x, device_y = 2244, 1080


# 刷金币次数
repeat_times = 60

# 日志输出
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)


def tap_screen(x, y):
    """calculate real x, y according to device resolution."""
    base_x, base_y = 2244, 1080
    real_x = int(x / base_x * device_x)
    real_y = int(y / base_y * device_y)
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


if __name__ == '__main__':
    while True:
        action = check_action()
        take_action(action)
