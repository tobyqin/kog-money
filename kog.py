# -*- coding: utf-8 -*-

import logging
import os
from baseline import check_action, save_crop, convert_cord, init
import time
import datetime
from time import sleep

# 刷金币次数
repeat_times = 60

# 日志输出
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG
                    )


def tap_screen(x, y):
    """calculate real x, y according to device resolution."""
    real_x, real_y = convert_cord(x, y)
    cmd = 'adb shell input tap {} {}'.format(real_x, real_y)
    logging.debug(cmd)
    os.system(cmd)


def take_action(action):
    global start
    global count
    if not action:
        return
    if action == 'restart':
        tap_screen(1877, 993)
    elif action == 'start':
        tap_screen(1600, 888)
    elif action in ['skip0', 'skip1']:
        tap_screen(2080, 44)
    elif action == 'continue':
        logging.info("round #{}, 花费时间: {}秒".format(count, time.time() - start))
        tap_screen(1074, 971)
        start = time.time()
        count = count + 1
        if count > repeat_times: # 到达指定次数后退出
            exit(0)
    elif action == 'exit':
        tap_screen(1950, 100)

    sleep(1)


if __name__ == '__main__':
    init()
    save_crop()
    count = 0
    start = time.time()
    logging.info("start at: {}".format(datetime.datetime.now()))
    while True:
        action = check_action()
        take_action(action)
