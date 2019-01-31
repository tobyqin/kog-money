import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage.feature import match_template
import glob
from util import pull_screenshot, SCREEN_PATH, swipe, tap_center, hero_anchor
import time
from pypinyin import pinyin

OPENCV = 0
SKIMAGE = 1

lib = OPENCV


def match_template1(template, img, plot=False, method=cv2.TM_SQDIFF_NORMED):
    img = cv2.imread(img, 0).copy()
    template = cv2.imread(template, 0)
    w, h = template.shape[::-1]
    if lib == OPENCV:
        res = cv2.matchTemplate(img, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
    else:
        result = match_template(img, template)
        ij = np.unravel_index(np.argmax(result), result.shape)
        top_left = ij[::-1]

    bottom_right = (top_left[0] + w, top_left[1] + h)

    if plot:
        cv2.rectangle(img, top_left, bottom_right, 255, 5)
        plt.subplot(121)
        plt.imshow(img)
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.subplot(122)
        plt.imshow(template)

        plt.show()

    return top_left, bottom_right


method = 'cv2.TM_SQDIFF'
template = 'img/crop_start.png'
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']


def test():
    # for method in methods:
    # for template in glob.glob('img/crop*'):
    #     print(template)
    #     match_template1(template, 'screen.png', plot=True, method=eval(method))
    match_template1('img/hero/bailixuance.png','screen.png',plot=True, method=eval(method))
    for template in glob.glob('img/hero/*'):
        match_template1(template,'hero1.png',plot=True, method=eval(method))


def valid_hero_location(top_left):
    left = top_left[0]
    if abs(left - hero_anchor[0]) < hero_anchor[2] or abs(left - hero_anchor[1]) < hero_anchor[2]:
        return True
    return False


def swipe_hero(reverse=False):
    if reverse:
        swipe(65, 200, 65, 600, 1500)
    else:
        swipe(65, 600, 65, 200, 1500)


def chose_hero(name, reverse=False):
    template = 'img/hero/{}.png'.format(name)

    now = time.time()
    while True:
        pull_screenshot(save_file=True)
        top_left, bottom_right = match_template1(template, SCREEN_PATH)
        valid = valid_hero_location(top_left)
        if valid :
            break

        if time.time() - now > 30:
            return False
        swipe_hero(reverse=reverse)

    pull_screenshot(save_file=True)
    top_left, bottom_right = match_template1(template, SCREEN_PATH)
    tap_center(top_left, bottom_right)
    return True


def to_pinyin(name):
    n = [x for a in pinyin(name, 0) for x in a]
    return ''.join(n)

if __name__ == '__main__':
    chose_hero('老夫子')