from PIL import Image, ImageDraw
from fonts.fonts import *

import logging


class Widget(object):

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.data = None

    def refresh(self, image: Image, x: int, y: int):
        image.paste(self._refresh_image(), (x, y))

    def _refresh_image(self) -> Image:
        self.data = None
        image = Image.new('1', (self.width, self.height), 255)
        draw = ImageDraw.Draw(image)
        try:
            self._fetch()
        except Exception as ex:
            logging.exception(ex)
        if not self._has_data():
            draw.text((0, 0), 'Pas de donnée.', font=text_font_italic, fill='black')
            return image
        self._paint(draw)
        return image

    def _has_data(self):
        return self.data is not None

    def _fetch(self):
        pass

    def _paint(self, draw: ImageDraw):
        pass
