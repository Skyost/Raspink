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

openweathermap_font_map = {
    # Clear sky :
    '01d': 'f00d',
    '01n': 'f02e',
    # Few clouds :
    '02d': 'f002',
    '02n': 'f086',
    # Scattered clouds :
    '03d': 'f041',
    '03n': 'f041',
    # Broken clouds :
    '04d': 'f013',
    '04n': 'f013',
    # Shower rain :
    '09d': 'f009',
    '09n': 'f037',
    # Rain :
    '10d': 'f019',  # 'f008',
    '10n': 'f019',  # 'f036',
    # Thunderstorm :
    '11d': 'f01e',  # 'f010',
    '11n': 'f01e',  # 'f03b',
    # Snow :
    '13d': 'f01b',  # 'f00a',
    '13n': 'f01b',  # 'f038',
    # Mist :
    '50d': 'f003',
    '50n': 'f04a',
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
