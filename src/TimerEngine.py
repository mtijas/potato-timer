class TimerEngine:
    def __init__(self):
        self.timers = [("work", 20), ("pause", 5)]

    def getTimers(self):
        return self.timers
