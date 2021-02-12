import time

class TimerEngine:
  def __init__(self, config):
    self._config = config
    self._alarm_triggered = False
    self._work_count = 0
    self._short_count = 0
    self._long_count = 0
    self._others_count = 0
    self._current_timer_id = 0
    self._previous_monotonic = 0
    self._running = False
    self._started_at = None
    self._timer_name = None
    self._timer_duration = 0
    self._time_elapsed = 0
    self._total_time_elapsed = 0
    self._total_time_working = 0
    self._total_time_s_breaks = 0
    self._total_time_l_breaks = 0
    self._total_time_others = 0
    self.select_timer(0)

  """Acknowledge alarm"""
  def ack_alarm(self):
    self._alarm_triggered = False

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
      since_update = self.get_elapsed_time()
      self._time_elapsed += since_update
      self.calc_total_time_spent(since_update)
      if self._time_elapsed >= self._timer_duration:
        self._alarm_triggered = True
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
    self._current_timer_id += 1
    if self._current_timer_id >= len(self._config.timers):
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
    else:
      self._others_count += 1

  """Calculate total time elapsed and time spent working"""
  def calc_total_time_spent(self, since_update):
    if self._timer_name == "work":
      self._total_time_working += since_update
    elif self._timer_name == "short break":
      self._total_time_s_breaks += since_update
    elif self._timer_name == "long break":
      self._total_time_l_breaks += since_update
    else:
      self._total_time_others += since_update
    self._total_time_elapsed += since_update

  """Load timer from timers list"""
  def select_timer(self, timer_id):
    timer = self._config.get_timer(timer_id)
    self._timer_name = timer["type"]
    self._timer_duration = timer["duration"]*60
  
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
    return self._alarm_triggered

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
  def others_count(self):
    return self._others_count

  @property
  def total_time_working(self):
    return self._total_time_working

  @property
  def total_time_s_breaks(self):
    return self._total_time_s_breaks

  @property
  def total_time_l_breaks(self):
    return self._total_time_l_breaks

  @property
  def total_time_others(self):
    return self._total_time_others

  @property
  def total_time_elapsed(self):
    return self._total_time_elapsed

  @property
  def timer_duration(self):
    return self._timer_duration

  @property
  def time_elapsed(self):
    return self._time_elapsed