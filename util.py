from PIL import Image
import numpy as np
import os
import logging
import subprocess
from io import BytesIO
from adb.client import Client as AdbClient
client = AdbClient(host="127.0.0.1", port=5037)

device = client.devices()[0]

baseline = {}

SCREEN_PATH = 'screen.png'

tap_cords = {
    'restart': (1750, 950, 2000, 1040),
    'continue': (1000, 940, 1250, 1000),
    'start': (1475,  830, 1720, 920),
    'skip0': (2000, 29, 2100, 85),
    'skip1': (2025, 20, 2135, 70),
    'exit': (1890, 60, 2030, 145,),
    'start_match': (1100,860, 1400, 940),
    'return_room': (1150, 955, 1380,1025),
    'confirm': (1020, 255, 1250, 300),
    'match_continue': (970, 950, 1270, 1035),
    'recover': (1320, 930, 1380, 1000),
    'pick_hero': (1900, 990, 2140, 1060),
    'check_finished': (816, 656, 998, 693),
    'confirm_hero': (1900, 980, 2142, 1066)
    # 'expand_hero': (459, 483,494,602)
}


tap_only_cords = {
    'add_skill0': (1535, 810, 1595, 870),
    'add_skill1': (1650, 610, 1710, 670),
    'add_skill2': (1850, 490, 1910, 550),
    'buy_item': (2060, 145, 2110, 205)
}


# x, y, width, dura_start, dura_end - dura_start, 从点 x,y 随机方向滑动width，持续时间随机
swipe_cords = {
    'random_walk': (430, 850, 200, 3000, 8000),
    'skill0':(1670, 950, 200, 100, 400),
    'skill1':(1790, 750, 200, 100, 400),
    'skill2':(1990, 630, 200, 100, 400),
}

threshold = 10
ACTIONS = tap_cords.keys()

# 屏幕分辨率
device_x, device_y = 2244, 1080
base_x, base_y = 2244, 1080


def init():
    find_screen_size()


def convert_cord(x,y):
    real_x = int(x / base_x * device_x)
    real_y = int(y / base_y * device_y)
    return real_x, real_y


def tap_screen(x, y):
    """calculate real x, y according to device resolution."""
    real_x, real_y = convert_cord(x, y)
    device.shell('input tap {} {}'.format(real_x, real_y))


def tap_center(top_left, bottom_right):
    tap_screen((top_left[0] + bottom_right[0])/2, (top_left[1] + bottom_right[1])/2)


def tap_by_name(name):
    top_left = tap_cords[name][:2]
    bottom_right = tap_cords[name][2:]
    tap_center(top_left, bottom_right)


def swipe(x, y, x1, y1, duration):
    device.shell('input swipe {} {} {} {} {}'.format(x, y, x1, y1, duration))


def find_screen_size():
    global device_x
    global device_y
    img = pull_screenshot(False)
    device_x, device_y = img.size
    logging.info('device size x, y = ({}, {})'.format(device_x, device_y))


def save_crop():
    for key, val in tap_cords.items():
        img = Image.open('img/' + key + '.png')
        img.crop(val).save('img/crop_'+key+'.png')


def pull_screenshot(resize=False, method=0, save_file=False):
    if save_file and os.path.exists(SCREEN_PATH):
        os.remove(SCREEN_PATH)

    if method == 0:
        result = device.screencap()
        img = Image.open(BytesIO(result))

        if save_file:
            with open(SCREEN_PATH, "wb") as fp:
                fp.write(result)
    else:
        os.system('adb shell screencap -p /sdcard/screen.png')
        os.system('adb pull /sdcard/screen.png {}'.format(SCREEN_PATH))
        img = Image.open(SCREEN_PATH)

    if resize and img.size != (base_x, base_y):
        return img.resize((base_x, base_y))
    else:
        return img


def check_action():
    if not baseline:
        for n in ACTIONS:
            baseline[n] = np.array(Image.open('img/crop_' + n + '.png'))

    frame = pull_screenshot()

    crop_frame = {}
    for key, val in tap_cords.items():
        crop_frame[key] = np.sum(baseline[key] - np.array(frame.crop(val))) / baseline[key].size

    min_key = min(crop_frame, key=crop_frame.get)
    if crop_frame[min_key] < threshold:
        logging.info("ACTION: {}".format(min_key))
        return min_key

    logging.debug("ACTION: no action")

    return None


def check_single_action(name):
    if not baseline:
        for n in ACTIONS:
            baseline[n] = np.array(Image.open('img/crop_' + n + '.png'))

    frame = pull_screenshot()

    res = np.sum(baseline[name] - np.array(frame.crop(tap_cords[name]))) / baseline[name].size

    if res < threshold:
        return True

    return False
