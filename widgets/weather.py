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
        latitude = os.environ.get('WEATHER_LATITUDE')
        longitude = os.environ.get('WEATHER_LONGITUDE')
        if not latitude or not longitude:
            # Open-Meteo doesn't geolocate by IP itself, so we have to do it ourselves.
            location = requests.get('https://ipapi.co/json/').json()
            latitude = location['latitude']
            longitude = location['longitude']
        response = requests.get(
            'https://api.open-meteo.com/v1/forecast',
            params={
                'latitude': latitude,
                'longitude': longitude,
                'current': 'temperature_2m,apparent_temperature,weather_code,wind_speed_10m,relative_humidity_2m,is_day',
                'daily': 'weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset',
                'timezone': 'auto',
                'forecast_days': 4
            }
        ).json()
        current = Weather.from_current(response['current'])
        data.append(current)
        daily = response['daily']
        for index in range(len(daily['time'])):
            weather = Weather.from_daily(daily, index)
            if weather.date == current.date:
                current.temperature_min = weather.temperature_min
                current.temperature_max = weather.temperature_max
                current.sunrise = weather.sunrise
                current.sunset = weather.sunset
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
                'icon': u''
            },
            {
                'content': today.sunset.strftime('%H:%M'),
                'icon': u''
            },
            {
                'content': f'{round(today.wind_speed)} km/h',
                'icon': u''
            }
        ]
        for i in range(len(texts)):
            text = texts[i]
            spacing = 6
            (_, _, icon_width, icon_height) = draw.textbbox(xy=(0, 0), text=u'', font=weather_font_small)
            (_, _, text_width, text_height) = draw.textbbox(xy=(0, 0), text=text['content'], font=text_font)
            total_width = icon_width + text_width + spacing
            current_x = max_width - total_width
            current_y = i * (max(icon_height, text_height))
            draw.text((current_x, current_y + 6), text['icon'], font=weather_font_small, fill='black')
            current_y += text_height / 2
            draw.text((current_x + icon_width + spacing, current_y), text['content'], font=text_font, fill='black')


class Weather(object):

    def __init__(
        self,
        date: datetime.date,
        sunrise: datetime.datetime,
        sunset: datetime.datetime,
        temperature: float,
        temperature_feels_like: float,
        temperature_min: float,
        temperature_max: float,
        wind_speed: float,
        humidity: float,
        weather_code: int,
        is_day: bool = True
    ):
        self.date = date
        self.sunrise = sunrise
        self.sunset = sunset
        self.temperature = temperature
        self.temperature_feels_like = temperature_feels_like
        self.temperature_min = temperature_min
        self.temperature_max = temperature_max
        self.wind_speed = wind_speed
        self.humidity = humidity
        self.icon = chr(int(open_meteo_font_map[weather_code][0 if is_day else 1], 16))

    @staticmethod
    def from_current(json_object: dict) -> 'Weather':
        return Weather(
            date=datetime.datetime.fromisoformat(json_object['time']).date(),
            sunrise=None,
            sunset=None,
            temperature=json_object['temperature_2m'],
            temperature_feels_like=json_object['apparent_temperature'],
            temperature_min=None,
            temperature_max=None,
            wind_speed=json_object['wind_speed_10m'],
            humidity=json_object['relative_humidity_2m'],
            weather_code=json_object['weather_code'],
            is_day=bool(json_object['is_day'])
        )

    @staticmethod
    def from_daily(json_object: dict, index: int) -> 'Weather':
        return Weather(
            date=datetime.date.fromisoformat(json_object['time'][index]),
            sunrise=datetime.datetime.fromisoformat(json_object['sunrise'][index]),
            sunset=datetime.datetime.fromisoformat(json_object['sunset'][index]),
            temperature=json_object['temperature_2m_max'][index],
            temperature_feels_like=None,
            temperature_min=json_object['temperature_2m_min'][index],
            temperature_max=json_object['temperature_2m_max'][index],
            wind_speed=None,
            humidity=None,
            weather_code=json_object['weather_code'][index],
            is_day=True
        )
