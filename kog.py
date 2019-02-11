# -*- coding: utf-8 -*-

import datetime
import logging

from action import get_action_by_name
from policy import get_policy
from util import save_crop, init

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
