# -*- coding: utf-8 -*-

import wda
import logging
import os
import random
from time import sleep
import time
# 日志输出
logging.basicConfig(format='[%(asctime)s][%(name)s:%(levelname)s(%(lineno)d)][%(module)s:%(funcName)s]:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S',
                    level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)

# 屏幕分辨率
device_x, device_y = 1920, 1080

# 小号 60左右 da 30
FIGHT_TIME = 30

# 刷金币次数
repeat_times = 60

c = wda.Client()
s = c.session()

#===============================
# home键在左方
# 按钮:再次挑战
# (650,130) (710,310)
def rechallenge_btn():
    x = random.uniform(650,710)
    y = random.uniform(130,310)
    logging.info("点击重新挑战按钮 [{},{}]".format(x,y))
    return (x,y)
# 按钮:闯关 
# (600,220)  (670,400)
def start_btn():
    x = random.uniform(600,670)
    y = random.uniform(220,400)
    logging.info("点击开始按钮 [{},{}]".format(x,y))
    return (x,y)
# 按钮: 平A 640,115 r=50
def attack_btn():
    return circle_btn(640,115,50)
# 按钮: 技能1 660,345 r=35
def skill_one_btn():
    return circle_btn(660,345,35)
# 按钮: 技能2 515,255 r=35
def skill_two_btn():
    return circle_btn(515,225,35)
# 按钮: 技能3 435,120 r=35
def skill_three_btn():
    return circle_btn(435,120,35)

def circle_btn(rx,ry,r):
    x=6666
    y=2333
    while x*x+y*y > 5000:
        x = random.uniform(-r,r)
        y = random.uniform(-r,r)

    return (rx+x,ry+y)

skill_cool_down_time = {
    "skill_one_btn":time.time()-100,
    "skill_two_btn":time.time()-100,
    "skill_three_btn":time.time()-100,
}

skill_cool_down = {
    "skill_one_btn":8,
    "skill_two_btn":14,
    "skill_three_btn":25,
}

skills = {
    "skill_one_btn":skill_one_btn(),
    "skill_two_btn":skill_two_btn(),
    "skill_three_btn":skill_three_btn(),
}

def do_attack_random():
    choice = random.randint(0,3)
    if choice==0:
        return attack_btn()
    elif choice==1:
        return skill_one_btn()
    elif choice==2:
        return skill_two_btn()
    elif choice==3:
        return skill_three_btn()

def do_attack():
    now = time.time()
    for i in skill_cool_down:
        if now - skill_cool_down[i] > skill_cool_down_time[i]:
            skill_cool_down_time[i] = now
            logging.debug("click {}".format(i))
            return skills[i]
    logging.debug("click {}".format("attack_btn"))
    return attack_btn()


def tap_screen(func):
    """calculate real x, y according to device resolution."""
    pair = func()
    x=pair[0]
    y=pair[1]
    base_x, base_y = 1920, 1080
    real_x = int(x / base_x * device_x)
    real_y = int(y / base_y * device_y)
    # os.system('adb shell input tap {} {}'.format(real_x, real_y))
    logging.debug("tap ({},{})".format(real_x,real_y))
    s.tap_hold(real_x, real_y, 20/1000 )


def do_money_work():

    #开始闯关
    tap_screen(start_btn)
    #载入画面
    sleep(4)

    # 战斗场景
    start = time.time()
    while time.time() - start < FIGHT_TIME:
        tap_screen(do_attack)
        sleep(random.uniform(0.2,0.4))

    tap_screen(rechallenge_btn)
    sleep(2)


if __name__ == '__main__':
    mstart = time.time()
    mround = 0
    try:
        for i in range(repeat_times):
            mround = i+1
            logging.info('round #{}'.format(i + 1))
            do_money_work()
    except KeyboardInterrupt as k:
        pass
    finally:
        logging.info("本次共进行{}轮游戏,总用时{}s,预计刷金币{}g".format(mround,time.time()-mstart,19*mround))
        logging.debug("关闭session")
        s.close()

