# -*- coding: utf-8 -*-

import logging
import os
from util import check_action, save_crop, convert_cord, init, tap_screen, check_single_action
from policy import get_policy
import time
import datetime
from action import get_action_by_name

# 刷金币次数
repeat_times = 60

# 日志输出
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO
                    )


def main():
    init()
    save_crop()
    logging.info("start at: {}".format(datetime.datetime.now()))
    play = get_policy()
    while True:
        action = play.action()
        if action:
            get_action_by_name(action).execute()



if __name__ == '__main__':
    main()
    