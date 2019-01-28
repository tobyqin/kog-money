# -*- coding: utf-8 -*-

import logging
import os
from util import check_action, save_crop, convert_cord, init, tap_screen
import time
import datetime
from time import sleep
from action import get_action_by_name

# 刷金币次数
repeat_times = 60

# 日志输出
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO
                    )


if __name__ == '__main__':
    init()
    save_crop()
    count = 0
    start = time.time()
    logging.info("start at: {}".format(datetime.datetime.now()))
    while True:
        action = check_action()
        if action:
            get_action_by_name(action).execute()
