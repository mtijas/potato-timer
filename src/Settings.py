class Settings:
  def __init__(self):
    self._alarm_type = "beep"
    self._use_colors = True
    self._timers = [
        {"type": "work", "duration": 0.2},
        {"type": "short break", "duration": 0.1},
        {"type": "long break", "duration": 0.3},
        {"type": "custom timer", "duration": 0.4}
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
