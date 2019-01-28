from PIL import Image
import numpy as np
import os
import logging
import subprocess
from io import BytesIO
from auto_adb import auto_adb
from adb.client import Client as AdbClient
client = AdbClient(host="127.0.0.1", port=5037)

adb = auto_adb()
device = client.devices()[0]

baseline = {}

SCREENSHOT_WAY = 3

boxes = {
    'restart': (1750, 950, 2000, 1040),
    'continue': (1000, 940, 1250, 1000),
    'start': (1475,  830, 1720, 920),
    'skip0': (2000, 29, 2100, 85),
    'skip1': (2025, 20, 2135, 70),
    'exit': (1890, 60, 2030, 145,)
}

threshold = 10
ACTIONS = boxes.keys()

# 屏幕分辨率
device_x, device_y = 2244, 1080


def convert_cord(x,y):
    base_x, base_y = 2244, 1080
    real_x = int(x / base_x * device_x)
    real_y = int(y / base_y * device_y)
    return real_x, real_y

def convert_box(a,b,c,d):
    a, b = convert_cord(a,b)
    c, d = convert_cord(c,d)
    return (a,b,c,d)


for key in boxes:
    boxes[key] = convert_box(*boxes[key])


def save_crop():
    for key, val in boxes.items():
        img = Image.open('img/' + key + '.png')
        img.crop(val).save('img/crop_'+key+'.png')


def pull_screenshot():
    global SCREENSHOT_WAY

    if SCREENSHOT_WAY == 0:
        os.system('adb shell screencap -p /sdcard/screen.png')
        os.system('adb pull /sdcard/screen.png')
        return Image.open('screen.png')
    elif 1 <= SCREENSHOT_WAY <= 3:
        return Image.open(BytesIO(device.screencap()))


def check_action():
    if not baseline:
        for n in ACTIONS:
            baseline[n] = np.array(Image.open('img/crop_' + n + '.png'))

    frame = pull_screenshot()

    crop_frame = {}
    for key, val in boxes.items():
        crop_frame[key] = np.sum(baseline[key] - np.array(frame.crop(val))) / baseline[key].size

    min_key = min(crop_frame, key=crop_frame.get)
    if crop_frame[min_key] < threshold:
        logging.info("ACTION: {}".format(min_key))
        return min_key

    return None
