# -*- coding: utf-8 -*-

import timeit
import logging
import os
from time import sleep
from PIL import Image
from baseline import check_action

# 屏幕分辨率
device_x, device_y = 2244, 1080

# 通关模式：1=重新挑战 -> 挑战界面，2=重新挑战-> 更换阵容
game_mode = 2

# 各步骤等待间隔
skip_wait = [10, 51, 16, 18]

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


def do_money_work():
    global game_mode
    if game_mode == 1: # 再次挑战
        logging.info('#0 restart challenge...')
        tap_screen(1877, 993)
        sleep(1)

    game_mode = 1
    logging.info('#1 start match!!!')
    tap_screen(1600, 888)   # 闯关，更换阵容
    sleep(1)

    for i in skip_wait:
        sleep(i)
        logging.info('skip conversation, interval {}s...'.format(i))
        tap_screen(2080, 44) # 跳过对话

    sleep(4)
    tap_screen(1074, 971) # 点击屏幕继续

    logging.info('#3 tap to continue...\n')
    sleep(3)


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
    # for i in range(repeat_times):
    #     logging.info('round #{}'.format(i + 1))
    #     do_money_work()
