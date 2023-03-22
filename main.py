from dotenv import load_dotenv
from display.factory import DisplayFactory
from raspink import Raspink

import argparse
import locale
import logging


def main(args):
    load_dotenv()
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    raspink = Raspink(DisplayFactory.create(args.display))
    raspink.start(args.schedule == 'true')


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(
            description='Raspink arguments',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument('--display', type=str, default='epd', help='Whether to run the script using shell or EPD.')
        parser.add_argument('--schedule', type=str, default='true', help='Whether to run the script continuously.')
        main(parser.parse_args())
    except KeyboardInterrupt:
        logging.info('Interrupted by keyboard.')
