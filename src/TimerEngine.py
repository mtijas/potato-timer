import time

class TimerEngine:
    def __init__(self):
        self.current_timer_id = 0
        self.previous_monotonic = 0
        self.running = False
        self.timers = [
                ("work", 20),
                ("pause", 5),
                ("work", 20),
                ("pause", 5),
                ("work", 20),
                ("long pause", 15),
        ]
        self.timer_name = None
        self.timer_duration = 0
        self.time_elapsed = 0
        self.select_timer(0)

    def start_timer(self):
        self.running = True
        self.previous_monotonic = time.monotonic()

    def stop_timer(self):
        self.running = False

    def update(self):
        if self.running:
            self.time_elapsed += self.get_elapsed_time()
            if self.time_elapsed >= self.timer_duration:
                self.time_elapsed = 0
                self.next_timer()

    def get_elapsed_time(self):
        current_m = time.monotonic()
        elapsed = (current_m - self.previous_monotonic)
        self.previous_monotonic = current_m
        return elapsed

    def next_timer(self):
        self.current_timer_id += 1
        if self.current_timer_id >= len(self.timers):
            self.current_timer_id = 0
        self.select_timer(self.current_timer_id)

    def select_timer(self, timer_id):
        if timer_id < len(self.timers):
            self.timer_name, self.timer_duration = self.timers[timer_id]
        else:
            raise IndexError("Timer not found")

    def reset_timer(self):
        self.time_elapsed = 0

