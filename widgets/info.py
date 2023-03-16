import datetime
import subprocess

from PIL import ImageDraw
from fonts.fonts import *
from widgets.widget import Widget


class InfoWidget(Widget):

    def __init__(self):
        super(InfoWidget, self).__init__(800, 14)

    def _fetch(self):
        try:
            output = subprocess.check_output(['sudo', 'iwgetid']).decode('utf-8')
            self.data = DeviceInfo(output.split('"')[1], datetime.datetime.now())
        except FileNotFoundError:
            self.data = DeviceInfo('Inconnu', datetime.datetime.now())

    def _paint(self, draw: ImageDraw):
        font_size = 12
        icon_font_tiny = icon_font.font_variant(size=font_size)
        text_font_tiny = text_font.font_variant(size=font_size)
        text_font_italic_tiny = text_font_italic.font_variant(size=font_size)

        # Wifi name :
        icon = u'\uf1eb'
        (icon_width, icon_height) = draw.textsize(icon, font=icon_font_tiny)
        draw.text((0, 2), icon, font=icon_font_tiny, fill='black')
        draw.text((icon_width + 6, 0), self.data.wifi, font=text_font_tiny, fill='black')

        # Last updated :
        text = self.data.date.strftime('%d/%m/%Y %H:%M:%S')
        (text_width, text_height) = draw.textsize(text, font=text_font_italic_tiny)
        draw.text((self.width - text_width, 0), text, font=text_font_italic_tiny, fill='black')


class DeviceInfo(object):

    def __init__(self, wifi: str, date: datetime):
        self.wifi = wifi
        self.date = date
