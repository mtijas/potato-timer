import time

class TimerEngine:
  def __init__(self):
    self.alarm = False
    self.work_count = 0
    self.short_count = 0
    self.long_count = 0
    self.current_timer_id = 0
    self.previous_monotonic = 0
    self.running = False
    self.started_at = None
    self.timers = [
        ("work", 2),
        ("short break", 1),
        ("work", 2),
        ("kissat koiria", 0.1),
        ("work", 2),
        ("short break", 1),
        ("work", 2),
        ("long break", 3),
    ]
    self.timer_name = None
    self.timer_duration = 0
    self.time_elapsed = 0
    self.total_time_elapsed = 0
    self.total_time_working = 0
    self.select_timer(0)

  def ack_alarm(self):
    self.alarm = False

  def start_timer(self):
    self.running = True
    self.previous_monotonic = time.monotonic()
    if self.started_at == None:
      self.started_at = time.localtime()

  def stop_timer(self):
    self.running = False

  def update(self):
    if self.running:
      self.time_elapsed += self.get_elapsed_time()
      if self.time_elapsed >= self.timer_duration:
        self.alarm = True
        self.increase_counts()
        self.next_timer()
        self.time_elapsed = 0

  def get_elapsed_time(self):
    current_m = time.monotonic()
    elapsed = (current_m - self.previous_monotonic)
    self.previous_monotonic = current_m
    return elapsed

  def next_timer(self):
    self.calc_stats()
    self.current_timer_id += 1
    if self.current_timer_id >= len(self.timers):
      self.current_timer_id = 0
    self.select_timer(self.current_timer_id)

  def increase_counts(self):
    if self.timer_name == "work":
      self.work_count += 1
    elif self.timer_name == "short break":
      self.short_count += 1
    elif self.timer_name == "long break":
      self.long_count += 1

  def calc_stats(self):
    if self.timer_name == "work":
      self.total_time_working += self.time_elapsed
    self.total_time_elapsed += self.time_elapsed

  def select_timer(self, timer_id):
    if timer_id < len(self.timers):
      name, duration = self.timers[timer_id]
      self.timer_name = name
      self.timer_duration = duration*60
    else:
      raise IndexError("Timer not found")

  def reset_timer(self):
    self.time_elapsed = 0

