from display.display import Display


class DisplayFactory(object):

    @staticmethod
    def create(name: str) -> 'Display':
        if name == 'shell':
            from display.shell import ShellDisplay
            return ShellDisplay()
        else:
            from display.epd import EPDDisplay
            return EPDDisplay()
