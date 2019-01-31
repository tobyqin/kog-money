from util import tap_screen, swipe
from kog import main
import time


def tap_sleep(x,y):
    tap_screen(x,y)

    time.sleep(0.5)


if __name__ == '__main__':
    tap_sleep(1007, 531)

    tap_sleep(784, 379)

    tap_sleep(658, 346)

    swipe(313, 582, 318, 250, 500)

    tap_sleep(681, 377)

    tap_sleep(1006, 610)

    main()
