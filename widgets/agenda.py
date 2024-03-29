import os
import requests
import datetime
import recurring_ical_events

from icalendar import Calendar
from PIL import ImageDraw
from fonts.fonts import *
from widgets.widget import Widget


class AgendaWidget(Widget):

    def __init__(self):
        super(AgendaWidget, self).__init__(380, 284)

    def _fetch(self):
        self.data = {}
        ical = requests.get(os.environ['ICAL_URL']).text
        calendar = Calendar.from_ical(ical)
        now = datetime.datetime.now()
        current_year = now.strftime('%Y')
        current_month_day = now.strftime('%m%d')
        events = recurring_ical_events.of(calendar).between(
            current_year + current_month_day,
            str(int(current_year) + 1) + ('0301' if current_month_day == '0229' else current_month_day)
        )
        for event in events:
            key = event.decoded('DTSTART')
            if isinstance(key, datetime.datetime):
                key = key.date()
            if key in self.data:
                date_events = self.data[key]
            else:
                date_events = []
                self.data[key] = date_events
            date_events.append({
                'name': event.decoded('SUMMARY').decode('UTF-8'),
                'start': event.decoded('DTSTART'),
                'end': event.decoded('DTEND'),
            })
            self.data[key] = sorted(
                date_events,
                key=lambda x: (datetime.datetime.combine(x['start'], datetime.time(23, 0)) if isinstance(x['start'], datetime.date) else x['start'], x['name'])
            )
        self.data = dict(sorted(self.data.items()))

    def _paint(self, draw: ImageDraw):
        current_y = 0
        icon_font_small = icon_font.font_variant(size=30)
        icon_font_big = icon_font.font_variant(size=34)

        # Title :
        icon = u'\uf073'
        title = 'Agenda'
        (_, _, icon_width, icon_height) = draw.textbbox(xy=(0, 0), text=icon, font=icon_font_small)
        (_, _, title_width, title_height) = draw.textbbox(xy=(0, 0), text=title, font=title_font)
        draw.text((0, current_y), icon, font=icon_font_big, fill='black')
        draw.text((icon_width + 16, current_y - 4), title, font=title_font, fill='black')
        current_y += max(icon_height, title_height) + 8

        # If no task :
        if len(self.data) == 0:
            text = 'Rien à faire'
            (_, _, text_width, text_height) = draw.textbbox(xy=(0, 0), text=text, font=text_font_italic)
            draw.text(((self.width - text_width) / 2, (self.height - text_height) / 2), text, font=text_font_italic,
                      fill='black')
            return

        # Ellipsis size :
        ellipsis_text = '...'
        (_, _, ellipsis_width, ellipsis_height) = draw.textbbox(xy=(0, 0), text=ellipsis_text, font=text_font)

        # Agenda content :
        for date, events in self.data.items():
            formatted_date_text = word_wrap(draw, date.strftime('%d/%m/%Y'), self.width)
            (_, _, text_width, text_height) = draw.textbbox(xy=(0, 0), text=formatted_date_text, font=text_font)
            if self.height > current_y + text_height:
                date_y = current_y
                current_y += text_height + 6
                events_to_draw = len(events)
                events_drawn = 0
                for event in events:
                    spacing = 24
                    event_name = event['name']
                    if isinstance(event['start'], datetime.datetime):
                        event_name = event['start'].strftime('%H:%M') + '  ' + event_name
                    text = word_wrap(draw, event_name, self.width - spacing)
                    (_, _, text_width, text_height) = draw.textbbox(xy=(0, 0), text=text, font=text_font)
                    if self.height > current_y + text_height \
                            or (events_drawn >= events_to_draw - 1 and self.height > current_y + text_height):
                        draw.text((0, current_y), '—', font=text_font, fill='black')
                        draw.text((spacing, current_y), text, font=text_font, fill='black')
                        current_y += text_height + 6
                        events_drawn += 1
                if events_drawn > 0:
                    draw.text((0, date_y), formatted_date_text, font=text_font, fill='black')
                    if events_drawn < events_to_draw:
                        draw.text(((self.width - ellipsis_width) / 2, self.height - ellipsis_height), ellipsis_text,
                                  font=text_font, fill='black')
