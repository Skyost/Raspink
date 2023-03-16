from PIL import ImageDraw
from widgets.widget import Widget


class HorizontalRuleWidget(Widget):

    def __init__(self):
        super(HorizontalRuleWidget, self).__init__(380, 2)

    def _has_data(self):
        return True

    def _paint(self, draw: ImageDraw):
        draw.line([(0, 0), (self.width, 0)], fill='black', width=2)
