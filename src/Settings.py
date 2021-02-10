class Settings:
  def __init__(self):
    self._alarm_type = "beep"
    self._use_colors = True
    self._timers = [
        ("work", 25),
        ("short break", 5),
        ("work", 25),
        ("short break", 5),
        ("work", 25),
        ("short break", 5),
        ("work", 25),
        ("long break", 35),
    ]

  """Get timer by id"""
  def get_timer(self, timer_id):
    if timer_id < len(self._timers):
      return self._timers[timer_id]
    else:
      raise IndexError("Timer not found")

  @property
  def timers(self):
    return self._timers

  @property
  def use_colors(self):
    return self._use_colors

  @property
  def alarm_type(self):
    return self._alarm_type
