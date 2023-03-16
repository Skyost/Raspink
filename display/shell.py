from display.display import Display
from PIL import Image


class ShellDisplay(Display):

    def __init__(self):
        super().__init__(800, 480)

    def display(self, image: Image):
        image.show()
