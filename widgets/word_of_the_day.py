import feedparser
import html

from fonts.fonts import *
from widgets.widget import Widget
from PIL import ImageDraw


class WordOfTheDayWidget(Widget):

    def __init__(self):
        super(WordOfTheDayWidget, self).__init__(380, 100)

    def _fetch(self):
        news_feed = feedparser.parse('http://unmotparjour.fr/feed/')
        self.data = news_feed.entries[0] if len(news_feed.entries) > 0 else None

    def _paint(self, draw: ImageDraw):
        current_y = 0

        # Word :
        (text_width, text_height) = draw.textsize(self.data['title'], font=title_font)
        draw.text((0, current_y), '> ' + self.data['title'], font=title_font, fill='black')
        current_y += text_height + 8

        # Summary :
        summary_parts = self.data['summary'].split('.')
        summary = summary_parts[0] + '.'
        if len(summary_parts) > 1:
            summary += summary_parts[1] + '.'
        text = word_wrap(draw, html.unescape(summary), self.width)
        draw.text((0, current_y), text, font=text_font, fill='black')
