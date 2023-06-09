import requests

from PIL import ImageDraw
from fonts.fonts import *
from widgets.widget import Widget


class RandomQuoteWidget(Widget):

    def __init__(self):
        super(RandomQuoteWidget, self).__init__(380, 144)

    def _fetch(self):
        self.data = requests.get(
            'https://api.quotable.io/random',
            params={
                'maxLength': '100'
            },
        ).json()

    def _paint(self, draw: ImageDraw):
        icon_font_small = icon_font.font_variant(size=18)
        current_y = 0

        # Quotation mark :
        (quotation_width, quotation_height) = draw.textsize('"', font=icon_font_small)
        draw.text((0, 8), u'\uf10d', font=icon_font_small, fill='black')
        current_x = quotation_width + 18

        # Quote :
        text = word_wrap(draw, self.data['content'], self.width - current_x)
        (text_width, text_height) = draw.textsize(text, font=text_font_italic)
        draw.text((current_x, current_y), text, font=text_font_italic, fill='black')
        current_y += text_height + 8

        # Author :
        draw.text((current_x, current_y), f'> {self.data["author"]}', font=text_font_small, fill='black')
