from util import tap_screen, swipe
from kog import main
import time


def tap_sleep(x,y):
    tap_screen(x,y)

    time.sleep(0.5)


if __name__ == '__main__':
    tap_sleep(513, 534)

    tap_sleep(1090, 174)

    tap_sleep(200, 387)

    tap_sleep(217, 95)

    main()
