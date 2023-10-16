
class Timer:
    def __init__(self, start=3600):
        self.start = start
        self.accumulate_starts = {'start': self.start}

    def set_timer(self):

        return self.accumulate_starts.get('start')
