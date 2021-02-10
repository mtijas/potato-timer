import time

class TimerEngine:
  def __init__(self, settings):
    self._settings = settings
    self._alarm = False
    self._work_count = 0
    self._short_count = 0
    self._long_count = 0
    self._current_timer_id = 0
    self._previous_monotonic = 0
    self._running = False
    self._started_at = None
    self._timer_name = None
    self._timer_duration = 0
    self._time_elapsed = 0
    self._total_time_elapsed = 0
    self._total_time_working = 0
    self.select_timer(0)

  """Acknowledge alarm"""
  def ack_alarm(self):
    self._alarm = False

  """Start current timer"""
  def start_timer(self):
    self._running = True
    self._previous_monotonic = time.monotonic()
    if self._started_at == None:
      self._started_at = time.localtime()

  """Stop current timer"""
  def stop_timer(self):
    self._running = False

  """Update timer status
  # 
  # Calling update actually runs the timer.
  # Make sure to call update at least every few seconds
  """
  def update(self):
    if self._running:
      self._time_elapsed += self.get_elapsed_time()
      if self._time_elapsed >= self._timer_duration:
        self._alarm = True
        self.increase_counts()
        self.next_timer()
        self._time_elapsed = 0

  """Returns time elapsed since last call"""
  def get_elapsed_time(self):
    current_m = time.monotonic()
    elapsed = (current_m - self._previous_monotonic)
    self._previous_monotonic = current_m
    return elapsed

  """Jump to next timer
  # 
  # Loops the timers list indefinitely
  """
  def next_timer(self):
    self.calc_stats()
    self._current_timer_id += 1
    if self._current_timer_id >= len(self._settings.timers):
      self._current_timer_id = 0
    self.select_timer(self._current_timer_id)

  """Increase timer counts based on currently selected timer"""
  def increase_counts(self):
    if self._timer_name == "work":
      self._work_count += 1
    elif self._timer_name == "short break":
      self._short_count += 1
    elif self._timer_name == "long break":
      self._long_count += 1

  """Calculate total time elapsed and time spent working"""
  def calc_stats(self):
    if self._timer_name == "work":
      self._total_time_working += self._time_elapsed
    self._total_time_elapsed += self._time_elapsed

  """Load timer from timers list"""
  def select_timer(self, timer_id):
    name, duration = self._settings.get_timer(timer_id)
    self._timer_name = name
    self._timer_duration = duration*60
  
  """Reset current timer to beginning"""
  def reset_timer(self):
    self._time_elapsed = 0

  @property
  def running(self):
    return self._running

  @property
  def timer_name(self):
    return self._timer_name

  @property
  def current_timer_id(self):
    return self._current_timer_id

  @property
  def alarm(self):
    return self._alarm

  @property
  def started_at(self):
    return self._started_at

  @property
  def long_count(self):
    return self._long_count

  @property
  def short_count(self):
    return self._short_count

  @property
  def work_count(self):
    return self._work_count

  @property
  def total_time_working(self):
    return self._total_time_working

  @property
  def total_time_elapsed(self):
    return self._total_time_elapsed

  @property
  def timer_duration(self):
    return self._timer_duration

  @property
  def time_elapsed(self):
    return self._time_elapsed