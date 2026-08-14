from PIL import ImageFont

title_font = ImageFont.truetype(
    './fonts/lato.ttf', 40
)

text_font = ImageFont.truetype(
    './fonts/lato.ttf', 24
)

text_font_small = text_font.font_variant(size=16)

text_font_italic = ImageFont.truetype(
    './fonts/lato-italic.ttf', 24
)

text_font_italic_small = text_font_italic.font_variant(size=16)

weather_font = ImageFont.truetype(
    './fonts/weathericons.ttf', 24
)

icon_font = ImageFont.truetype(
    './fonts/fontawesome.ttf', 24
)

# Maps Open-Meteo WMO weather codes to (day icon, night icon) glyphs of `weathericons.ttf`.
# See https://open-meteo.com/en/docs#weathervariables for the WMO code list.
open_meteo_font_map = {
    0: ('f00d', 'f02e'),  # Clear sky
    1: ('f00d', 'f02e'),  # Mainly clear
    2: ('f002', 'f086'),  # Partly cloudy
    3: ('f013', 'f013'),  # Overcast
    45: ('f003', 'f04a'),  # Fog
    48: ('f003', 'f04a'),  # Depositing rime fog
    51: ('f019', 'f019'),  # Light drizzle
    53: ('f019', 'f019'),  # Moderate drizzle
    55: ('f019', 'f019'),  # Dense drizzle
    56: ('f019', 'f019'),  # Light freezing drizzle
    57: ('f019', 'f019'),  # Dense freezing drizzle
    61: ('f019', 'f019'),  # Slight rain
    63: ('f019', 'f019'),  # Moderate rain
    65: ('f019', 'f019'),  # Heavy rain
    66: ('f019', 'f019'),  # Light freezing rain
    67: ('f019', 'f019'),  # Heavy freezing rain
    71: ('f01b', 'f01b'),  # Slight snow fall
    73: ('f01b', 'f01b'),  # Moderate snow fall
    75: ('f01b', 'f01b'),  # Heavy snow fall
    77: ('f01b', 'f01b'),  # Snow grains
    80: ('f009', 'f037'),  # Slight rain showers
    81: ('f009', 'f037'),  # Moderate rain showers
    82: ('f009', 'f037'),  # Violent rain showers
    85: ('f01b', 'f01b'),  # Slight snow showers
    86: ('f01b', 'f01b'),  # Heavy snow showers
    95: ('f01e', 'f01e'),  # Thunderstorm
    96: ('f01e', 'f01e'),  # Thunderstorm with slight hail
    99: ('f01e', 'f01e'),  # Thunderstorm with heavy hail
}


def word_wrap(draw, text, max_width, font=text_font):
    remaining = max_width
    _, _, space_width, space_height = draw.textbbox(xy=(0, 0), text=' ', font=font)
    # use this list as a stack, push/popping each line
    output_text = []
    # split on whitespace...
    for word in text.split(None):
        _, _, word_width, word_height = draw.textbbox(xy=(0, 0), text=word, font=font)
        if word_width + space_width > remaining:
            output_text.append(word)
            remaining = max_width - word_width
        else:
            if not output_text:
                output_text.append(word)
            else:
                output = output_text.pop()
                output += ' %s' % word
                output_text.append(output)
            remaining = remaining - (word_width + space_width)
    return '\n'.join(output_text)
