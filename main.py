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
    raspink.start()


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(
            description='Raspink arguments',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument('--display', type=str, default='epd', help='Whether to run the script using shell or EPD.')
        main(parser.parse_args())
    except KeyboardInterrupt:
        logging.info('Interrupted by keyboard.')

# (WeatherWidget()).refresh(image, 0, 0)
# (HorizontalRuleWidget()).refresh(image, 0, 160)
# (TasksWidget()).refresh(image, 0, 180)
# (NewsWidget()).refresh(image, 420, 0)
# (HorizontalRuleWidget()).refresh(image, 420, 230)
# (WordOfTheDayWidget()).refresh(image, 420, 240)
# (HorizontalRuleWidget()).refresh(image, 420, 350)
# (RandomQuoteWidget()).refresh(image, 420, 360)
# (InfoWidget()).refresh(image, 0, 460)
