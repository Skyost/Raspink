import datetime
import os
import requests

from PIL import ImageDraw
from fonts.fonts import *
from widgets.widget import Widget


class WeatherWidget(Widget):

    def __init__(self):
        super(WeatherWidget, self).__init__(380, 160)

    def _fetch(self):
        data = []
        location = requests.get('http://ip-api.com/json/').json()
        response = requests.get(
            'https://api.openweathermap.org/data/2.5/onecall',
            params={
                'lat': location['lat'],
                'lon': location['lon'],
                'units': 'metric',
                'lang': 'fr',
                'exclude': '[minutely,hourly,alerts]',
                'APPID': os.environ['OPENWEATHERMAP_KEY']
            }
        ).json()
        current = Weather(response['current'])
        data.append(current)
        json_weathers = response['daily']
        # del json_weathers[0]
        del json_weathers[4:]
        for json_weather in json_weathers:
            weather = Weather(json_weather)
            if weather.date == current.date:
                current.temperature_min = weather.temperature_min
                current.temperature_max = weather.temperature_max
            else:
                data.append(weather)
        if len(data) > 0:
            self.data = data

    def _paint(self, draw: ImageDraw):
        current_y = 0
        today = self.data[0]
        weather_font_small = weather_font.font_variant(size=30)
        weather_font_big = weather_font.font_variant(size=34)

        # Today's weather :
        temperature = f'{str(round(today.temperature))}°'
        (_, _, icon_width, icon_height) = draw.textbbox(xy=(0, 0), text=today.icon, font=weather_font_small)
        (_, _, text_width, text_height) = draw.textbbox(xy=(0, 0), text=temperature, font=title_font)
        draw.text((0, current_y), today.icon, font=weather_font_big, fill='black')
        draw.text((icon_width + 16, current_y - 4), temperature, font=title_font, fill='black')
        current_y += max(icon_height, text_height) + 6

        # Today's feels like :
        feels_like = f'Ressenti : {str(round(today.temperature_feels_like))}°'
        (_, _, text_width, text_height) = draw.textbbox(xy=(0, 0), text=feels_like, font=text_font)
        draw.text((0, current_y), feels_like, font=text_font, fill='black')
        current_y += text_height + 4

        # Today's min & max :
        min_max = f'{str(round(today.temperature_min))}°  |  {str(round(today.temperature_max))}°'
        (_, _, text_width, text_height) = draw.textbbox(xy=(0, 0), text=min_max, font=text_font)
        draw.text((0, current_y), min_max, font=text_font, fill='black')
        current_y += text_height + 6

        # Next days weather :
        count = len(self.data) - 1
        max_width = 0
        for i in range(count):
            current_x = i * self.width / count
            weather = self.data[i + 1]

            # The icon :
            (_, _, icon_width, icon_height) = draw.textbbox(xy=(0, 0), text=weather.icon, font=weather_font_small)
            draw.text((current_x, current_y), weather.icon, font=weather_font_small, fill='black')
            text_y = current_y
            current_x += icon_width + 6

            # The day of week :
            day_of_week = weather.date.strftime('%a')
            (_, _, text_width, text_height) = draw.textbbox(xy=(0, 0), text=day_of_week, font=text_font)
            draw.text((current_x, text_y), day_of_week, font=text_font, fill='black')
            text_y += text_font.size + 2
            max_width = max(max_width, current_x + text_width)

            # The temperature :
            temperature = f'{round(weather.temperature)}°'
            (_, _, text_width, text_height) = draw.textbbox(xy=(0, 0), text=temperature, font=text_font_small)
            draw.text((current_x, text_y), temperature, font=text_font_small, fill='black')
            max_width = max(max_width, current_x + text_width)

        texts = [
            {
                'content': today.sunrise.strftime('%H:%M'),
                'icon': u'\uf051'
            },
            {
                'content': today.sunset.strftime('%H:%M'),
                'icon': u'\uf052'
            },
            {
                'content': f'{round(today.wind_speed * 3.6)} km/h',
                'icon': u'\uf050'
            }
        ]
        for i in range(len(texts)):
            text = texts[i]
            spacing = 6
            (_, _, icon_width, icon_height) = draw.textbbox(xy=(0, 0), text=u'\uf051', font=weather_font_small)
            (_, _, text_width, text_height) = draw.textbbox(xy=(0, 0), text=text['content'], font=text_font)
            total_width = icon_width + text_width + spacing
            current_x = max_width - total_width
            current_y = i * (max(icon_height, text_height))
            draw.text((current_x, current_y + 6), text['icon'], font=weather_font_small, fill='black')
            current_y += text_height / 2
            draw.text((current_x + icon_width + spacing, current_y), text['content'], font=text_font, fill='black')


class Weather(object):

    def __init__(self, json_object: dict):
        self.date = datetime.datetime.fromtimestamp(json_object['dt']).date()
        self.sunrise = datetime.datetime.fromtimestamp(json_object['sunrise'])
        self.sunset = datetime.datetime.fromtimestamp(json_object['sunset'])
        if isinstance(json_object['temp'], dict):
            self.temperature = json_object['temp']['day']
            self.temperature_feels_like = json_object['feels_like']['day']
            self.temperature_min = json_object['temp']['min']
            self.temperature_max = json_object['temp']['max']
        else:
            self.temperature = json_object['temp']
            self.temperature_feels_like = json_object['feels_like']
            # self.temperature_min = -1
            # self.temperature_max = -1
        self.wind_speed = json_object['wind_speed']
        self.humidity = json_object['humidity']
        self.description = json_object['weather'][0]['description']
        self.icon = chr(int(openweathermap_font_map[json_object["weather"][0]["icon"]], 16))
