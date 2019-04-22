from threading import Thread
import time


class LoopThread(Thread):
    def __init__(self, target, period):
        super(LoopThread, self).__init__()
        self.target = target
        self.running = True
        self.period = period

    def run(self):
        while self.running:
            self.target()
            time.sleep(self.period)

    def cancel(self):
        self.self.running
