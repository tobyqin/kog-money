import logging
import os
from time import sleep

device_x, device_y = 1920, 1080
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)


def tap_screen(x, y):
    """calculate real x, y according to device resolution."""
    base_x, base_y = 1920, 1080
    real_x = int(x / base_x * device_x)
    real_y = int(y / base_y * device_y)
    os.system('adb shell input tap {} {}'.format(real_x, real_y))


def do_money_work():
    logging.debug('#1 start the game')
    tap_screen(1600, 970)
    sleep(3)

    logging.debug('#2 ready, go!!!')
    tap_screen(1450, 910)
    sleep(12)

    logging.debug('#3 auto power on!')
    tap_screen(1780, 40)
    sleep(55)

    logging.debug('#4 well done!')
    tap_screen(940, 1000)
    sleep(3)

    logging.debug('#5 do it again...\n')
    tap_screen(1430, 980)
    sleep(3)


if __name__ == '__main__':
    for i in range(50):
        logging.info('round #{}'.format(i + 1))
        do_money_work()