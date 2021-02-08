class TimerEngine:
    def __init__(self):
        self.timers = [("work", 20), ("pause", 5)]
        self.running = False
        self.current_timer_id = 0
        self.time_elapsed = 0
        self.timer_duration = 0



    def get_timers(self):
        return self.timers



    def start_timer(self):
        self.running = True



    def stop_timer(self):
        self.running = False



    def update(self):
        if self.running:
            self.time_elapsed += 1
        if self.time_elapsed >= 5:
            self.time_elapsed = 0
            self.stop_timer()
