import datetime
import math

import feedparser

from PIL import ImageDraw

from fonts.fonts import *
from widgets.widget import Widget


class NewsWidget(Widget):

    def __init__(self):
        super(NewsWidget, self).__init__(380, 300)

    def _fetch(self):
        news_feed = feedparser.parse('https://www.lemonde.fr/rss/une.xml')
        self.data = news_feed.entries
        self.data.sort(key=lambda entry: entry.get('published_parsed', entry.get('updated_parsed')), reverse=True)

    def _paint(self, draw: ImageDraw):
        current_y = 0
        now = datetime.datetime.now()
        clock_size = 50

        # Today's date :
        day_of_week = now.strftime('%A')
        (text_width, text_height) = draw.textsize(day_of_week, font=text_font)
        draw.text((0, current_y), day_of_week, font=text_font, fill='black')
        current_y += text_height + 2
        day_month = now.strftime('%d %B')
        if day_month[0] == '0':
            day_month = day_month[1:]
        (text_width, text_height) = draw.textsize(day_month, font=title_font)
        draw.text((0, current_y), day_month, font=title_font, fill='black')
        current_y += text_height

        # Today's hour
        clock_x = self.width - clock_size
        clock_y = (current_y - clock_size) / 2
        for i in range(1, 4):
            draw.ellipse((clock_x + i, clock_y + i, clock_x + clock_size - i, clock_y + clock_size - i), outline='black')
        draw.line(NewsWidget.clock_hand([clock_x, clock_y], clock_size, (now.hour % 12 + now.minute / 60 + now.second / 3600) / 12, 16), fill='black', width=3)
        draw.line(NewsWidget.clock_hand([clock_x, clock_y], clock_size, (now.minute + now.second / 60) / 60, 20), fill='black', width=2)
        current_y += 8

        # Entries :
        for entry in self.data:
            spacing = 24
            text = word_wrap(draw, entry.title, self.width - spacing)
            (text_width, text_height) = draw.textsize(text, font=text_font)
            if self.height > current_y + text_height:
                draw.text((0, current_y), '—', font=text_font, fill='black')
                draw.text((spacing, current_y), text, font=text_font, fill='black')
                current_y += text_height + 6

    @staticmethod
    def clock_hand(position: [float, float], clock_size: float, completion: float, length: float):
        radian_angle = - math.pi / 2 + (completion * 2 * math.pi)
        x = clock_size / 2 + length * math.cos(radian_angle)
        y = clock_size / 2 + length * math.sin(radian_angle)
        return [(position[0] + clock_size / 2, position[1] + clock_size / 2), (position[0] + x, position[1] + y)]
