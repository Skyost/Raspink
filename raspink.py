from PIL import Image

from display.display import Display
from scheduler import Scheduler
from widgets.widget import Widget
from widgets.horizontal_rule import HorizontalRuleWidget
from widgets.info import InfoWidget
from widgets.news import NewsWidget
from widgets.agenda import AgendaWidget
from widgets.weather import WeatherWidget
from widgets.random_quote import RandomQuoteWidget
# Some other widgets are available : RTMTasksWidget and WordOfTheDayWidget.


class Raspink(object):

    def __init__(self, display: Display):
        self.display = display
        self.scheduler = Scheduler(self.refresh)
        self.widgets = []
        self._append_default_widgets()

    def _append_default_widgets(self):
        default_gap = 10
        horizontal_rule_widget = HorizontalRuleWidget()

        # First column :
        current_y = 0
        for widget in [
            WeatherWidget(),
            horizontal_rule_widget,
            AgendaWidget()  # You can use RTMTasksWidget() instead
        ]:
            self._append_widget(0, current_y, widget)
            current_y += widget.height + default_gap

        # Second column :
        current_y = 0
        for widget in [
            NewsWidget(),
            horizontal_rule_widget,
            # WordOfTheDayWidget(),
            # horizontal_rule_widget,
            RandomQuoteWidget()
        ]:
            self._append_widget(420, current_y, widget)
            current_y += widget.height + default_gap

        # Footer :
        self._append_widget(0, 460, InfoWidget())

    def _append_widget(self, x: int, y: int, widget: Widget):
        self.widgets.append({'x': x, 'y': y, 'widget': widget})

    def start(self, schedule: bool = True):
        self.refresh()
        if schedule:
            self.scheduler.start()

    def stop(self):
        self.scheduler.stop()

    def refresh(self) -> bool:
        image = Image.new('1', (self.display.width, self.display.height), 'white')
        # image.paste((255, 255, 255), [0, 0, self.display.width, self.display.height])
        for widget in self.widgets:
            widget['widget'].refresh(image, widget['x'], widget['y'])
        self.display.display(image)
        return True
