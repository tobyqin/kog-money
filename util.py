import logging
import os
import time
from io import BytesIO

import numpy as np
from PIL import Image
from adb.client import Client as AdbClient

client = AdbClient(host="127.0.0.1", port=5037)

device = client.devices()[0]

baseline = {}

SCREEN_PATH = 'screen.png'

hero_anchor = (10, 134, 5)

MODE = "COIN"

tap_cords = {
    'restart': (1000, 635, 1170, 690),
    'continue': (560, 630, 720, 657),
    'start': (880,  555, 1035, 611),
    'skip0': (1190, 12, 1260, 45),
    'skip1': (1190, 12, 1260, 45),
    'exit': (1153, 43, 1264, 93,),
    'start_match': (630, 574, 822, 630),
    'return_room': (461, 638, 612, 684),
    'confirm': (572, 168, 709, 198),
    'match_continue': (542, 635, 739, 690),
    'recover': (710, 619, 757, 671),
    'pick_hero': (1104, 655, 1267, 712),
    'check_finished': (435, 442, 513, 459),
    'confirm_hero': (1103, 658, 1266, 713),
    'relax': (807, 457, 926, 508),
    'confirm1': (554, 635, 722, 693),
    'confirm2': (556, 477, 723, 528)
    # 'expand_hero': (459, 483,494,602)
}

tap_only_cords = {
    'add_skill0': (860, 540, 900, 580),
    'add_skill1': (940, 409, 980, 449),
    'add_skill2': (1067, 331, 1107, 371),
    'buy_item': (1205, 95, 1255, 137)
}


# x, y, width, dura_start, dura_end - dura_start, 从点 x,y 随机方向滑动width，持续时间随机
swipe_cords = {
    'random_walk': (220, 570, 130, 3000, 8000),
    'skill0':(943, 586, 85, 100, 400),
    'skill1':(1030, 500, 85, 100, 400),
    'skill2':(1121, 397, 85, 100, 400),
}

threshold = 10
ACTIONS = tap_cords.keys()

# 屏幕分辨率
device_x, device_y = 1280, 720
base_x, base_y = 1280, 720


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


def stop_game():
    device.shell('am force-stop com.tencent.tmgp.sgame')  # 关闭游戏


def start_game():
    device.shell('monkey -p com.tencent.tmgp.sgame -c android.intent.category.LAUNCHER 1')  # 打开游戏

    time.sleep(60)

    tap_screen(643, 553)

    logging.info("等待1分钟")

    time.sleep(60)

    logging.info("关闭广告")
    for i in range(5):  # 关闭广告
        tap_screen(1174, 77)


def restart_game():
    stop_game()

    logging.info("休息10分钟")
    time.sleep(60 * 10)

    logging.info("重启游戏")

    start_game()


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
        logging.debug("ACTION: {}".format(min_key))
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


def generate_hero_img():
    frame = pull_screenshot(save_file=True)
    y = 72
    h = 138
    x = 10
    w = 120
    row_num = 9
    col_num = 4

    base = 0

    if not os.path.exists('hero'):
        os.mkdir('hero')

    for j in range(col_num):
        for i in range(row_num):
            x_start = x + i * w
            y_start = y + j * h
            y_end = y_start + 100
            x_end = x_start + 100
            frame.crop((x_start, y_start, x_end, y_end)).save("hero/{}.png".format(j * row_num + i + base))


if __name__ == '__main__':
    # generate_hero_img()
    restart_game()
