import time
from datetime import datetime
from threading import Thread
from typing import Callable


class Scheduler(object):

    def __init__(self, action: Callable[[], bool]):
        self.current_thread = None
        self.is_stopped = False
        self.action = action

    def start(self) -> Thread:
        if self.current_thread is not None and self.current_thread.is_alive():
            return self.current_thread
        self.current_thread = Thread(target=self.schedule)
        self.current_thread.start()
        return self.current_thread

    def stop(self):
        self.is_stopped = True

    def schedule(self):
        now = datetime.now()
        time.sleep((5 - (now.minute % 5)) * 60 - now.second)
        while not self.is_stopped:
            if not self.action():
                self.stop()
                print('Scheduler stopped.')
                break
            now = datetime.now()
            time.sleep((5 - (now.minute % 5)) * 60 - now.second)
