from PIL import Image


class Display(object):

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def display(self, image: Image):
        pass
