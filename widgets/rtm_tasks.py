import os
import requests

from hashlib import md5
from PIL import ImageDraw
from fonts.fonts import *
from widgets.widget import Widget


class RTMTasksWidget(Widget):

    def __init__(self):
        super(RTMTasksWidget, self).__init__(380, 284)

    def _fetch(self):
        params = {
            'api_key': os.environ['REMEMBERTHEMILK_KEY'],
            'auth_token': os.environ['REMEMBERTHEMILK_TOKEN'],
            'format': 'json',
            'method': 'rtm.tasks.getList',
        }
        params.update({'api_sig': RTMTasksWidget._calculate_signature(params)})
        response = requests.get(
            'https://api.rememberthemilk.com/services/rest/',
            params=params
        ).json()['rsp']
        if response['stat'] != 'ok':
            return
        self.data = []
        for json_list in response['tasks']['list']:
            self.parse_json_list(json_list)

    def _paint(self, draw: ImageDraw):
        current_y = 0

        # Title :
        title = 'À faire'
        (_, _, title_width, title_height) = draw.textbbox(xy=(0, 0), text=title, font=title_font)
        draw.text((0, current_y), title, font=title_font, fill='black')
        current_y += title_height + 8

        # If no task :
        if len(self.data) == 0:
            text = 'Aucune tâche. Bravo Hugo !'
            (_, _, text_width, text_height) = draw.textbbox(xy=(0, 0), text=text, font=text_font_italic)
            draw.text(((self.width - text_width) / 2, (self.height - text_height) / 2), text, font=text_font_italic, fill='black')
            return

        # Subtitle :
        subtitle = f'{len(self.data)} ' + ('tâches' if len(self.data) > 1 else 'tâche')
        (_, _, subtitle_width, subtitle_height) = draw.textbbox(xy=(0, 0), text=subtitle, font=text_font_italic_small)
        draw.text((0, current_y), subtitle, font=text_font_italic_small, fill='black')
        current_y += subtitle_height + 8

        # Ellipsis size :
        ellipsis_text = '...'
        (_, _, ellipsis_width, ellipsis_height) = draw.textbbox(xy=(0, 0), text=ellipsis_text, font=text_font)

        # Tasks :
        tasks_to_draw = len(self.data)
        tasks_drawn = 0
        for task in self.data:
            spacing = 24
            text = word_wrap(draw, task, self.width - spacing)
            (_, _, text_width, text_height) = draw.textbbox(xy=(0, 0), text=text, font=text_font)
            if self.height - ellipsis_height > current_y + text_height \
                    or (tasks_drawn >= tasks_to_draw - 1 and self.height > current_y + text_height):
                draw.text((0, current_y), '—', font=text_font, fill='black')
                draw.text((spacing, current_y), text, font=text_font, fill='black')
                current_y += text_height + 6
                tasks_drawn += 1
        if tasks_drawn < tasks_to_draw:
            draw.text(((self.width - ellipsis_width) / 2, self.height - ellipsis_height), ellipsis_text, font=text_font, fill='black')

    def parse_json_list(self, json_list: dict):
        if 'taskseries' in json_list:
            for task in json_list['taskseries']:
                subtasks = task['task']
                should_add = True
                for subtask in subtasks:
                    if len(subtask['completed']) > 0 or len(subtask['deleted']) > 0:
                        should_add = False
                if should_add:
                    self.data.append(task['name'])

    @staticmethod
    def _calculate_signature(params: dict):
        result = os.environ['REMEMBERTHEMILK_SECRET']
        for key in sorted(params):
            result += (key + params[key])
        return md5(result.encode('utf-8')).hexdigest()
