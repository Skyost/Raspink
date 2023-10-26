from waveshare_epd import epd7in5
from display.display import Display
from PIL import Image


class EPDDisplay(Display):

    def __init__(self):
        self.epd = epd7in5.EPD()
        super().__init__(self.epd.width, self.epd.height)

    def display(self, image: Image):
        self.epd.init()
        self.epd.Clear()
        self.epd.display(self.epd.getbuffer(image))
        self.epd.sleep()

