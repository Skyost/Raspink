# Raspink

Raspink is a little utility that allows to display various info
on an eInk reader connected to a Raspberry Pi.

<img src="https://github.com/Skyost/Raspink/raw/master/screenshot.png" width="40%"> <img src="https://github.com/Skyost/Raspink/raw/master/preview.gif" width="40%">

I've been using it for my personal needs since the very start of 2022, and I've decided to share it.
As it is a personal utility, you may have to [customize it](#Customization) in order to suit your needs.

## Features

* Can fetch and display the weather for the next three days.
* Can fetch and display an iCal.
* Can fetch and display a random quote.
* Can fetch and display an RSS news feed.
* Can fetch and display... well almost what you want !

## Installation

### Prerequisites

I assume that your Waveshare EPD has been set up using [the official instructions](https://www.waveshare.com/wiki/Template:Raspberry_Pi_Guides_for_SPI_e-Paper).

### Python dependencies

This utility depends on the following Python libraries :

* [Pillow](https://pypi.org/project/Pillow/).
* [feedparser](https://pypi.org/project/feedparser/).
* [requests](https://pypi.org/project/requests/).
* [python-dotenv](https://pypi.org/project/python-dotenv/).
* [icalendar](https://pypi.org/project/icalendar/).
* [recurring-ical-events](https://pypi.org/project/recurring-ical-events/).

You'll have to install of them first.

### Clone the repository

Clone the current repository, using something like this :

```shell
git clone https://github.com/Skyost/Raspink
```

### Install and set up the `waveshare_epd` Python dependency

You must copy the content of the [`waveshare_epd` folder](https://github.com/waveshare/e-Paper/tree/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd)
into the newly created Raspink folder.
This library has been made for the [Waveshare 7.5" EPD](https://www.waveshare.com/7.5inch-e-paper-hat.htm). If you plan
to use it with another reader, you must replace the `epd7in5` references to `whatever_epd_you_are_using` in the `display/epd.py` file.

### Set up environment variables

Create a `.env` file in the Raspink folder. Use it like this :

```properties
OPENWEATHERMAP_KEY=your_key
REMEMBERTHEMILK_KEY=your_key
REMEMBERTHEMILK_SECRET=your_secret
REMEMBERTHEMILK_TOKEN=your_token
ICAL_URL=your_ical_url
```

Here's a little documentation :

* `OPENWEATHERMAP_KEY` : Put your [OpenWeatherMap API key](https://openweathermap.org/appid) here. It will allow you to fetch and display the current weather.
* `REMEMBERTHEMILK_KEY` : Put your [RememberTheMilk API key](https://www.rememberthemilk.com/services/api/) here. It will allow you to fetch and display your RTM tasks.
* `REMEMBERTHEMILK_SECRET` : Put your [RememberTheMilk shared secret](https://www.rememberthemilk.com/services/api/authentication.rtm) here. Works with `REMEMBERTHEMILK_KEY`.
* `REMEMBERTHEMILK_TOKEN` : Put your [RememberTheMilk authentication token](https://www.rememberthemilk.com/services/api/authentication.rtm) here. Works with `REMEMBERTHEMILK_KEY`.
* `ICAL_URL` : Put your iCal calendar URL here. Works best with Google Agenda calendars.

## Usage

Start Raspink by running the following command in the Raspink folder :

```shell
python ./main.py
```

With this command, the content is refreshed every five minutes. You can combine it with `nohup` to leave it active in the background.
Good for you : I've already done the work !

```shell
chmod +x start.sh
./start.sh
```

_Hey, don't run unverified scripts on your Pi !_

If you want to test it on Windows (for example), you may want to try this command :

```shell
python ./main.py --display=shell
```

## Customization

Feel free to customize Raspink and to add new features !
All displayed components are called ``Widgets'' and are available in the `widgets` folder.
They have two main methods :

* `_fetch()` that fetch remote data.
* `_paint(image)` that display the fetched data on the `image`.

You may be particularly interested in customizing the followings :

* _News_ (`news.py`) : The RSS feed URL is hardcorded. Change it here.
* _Word of the day_ (`word_of_the_day.py`) : The RSS feed URL is also hardcorded here.

The method `_append_default_widgets()` of the file `raspink.py` handles the displaying and
the placing of all widgets.
