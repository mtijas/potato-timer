import yaml
from pathlib import Path

class Config:
  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    pass
  
  def __init__(self, config_file = None):
    self._alarm_type = "beep"
    self._use_colors = True
    self._alarm_repeat = 1
    self._timers = [
        {"type": "work", "duration": 0.2},
        {"type": "short break", "duration": 0.1},
        {"type": "long break", "duration": 0.3},
        {"type": "custom timer", "duration": 0.4}
    ]
    self._possible_files = [
      "~/.config/mti-tomato-timer/config.yml",
      "~/.mti-tomato-timer-config.yml",
      "./config.yml",
    ]
    self._selected_config = self.find_config(config_file)
    if self._selected_config is not None:
      self.read_config()

  """Try to find config file"""
  def find_config(self, config_file):
    if config_file is not None:
      config_file = config_file.replace('~', str(Path.home()), 1)
      if Path(config_file).is_file():
        return config_file
    
    for possibility in self._possible_files:
      possibility = possibility.replace('~', str(Path.home()), 1)
      if Path(possibility).is_file():
        return possibility
    
    return None


  """Load the config file"""
  def read_config(self):
    with open(self._selected_config, 'r') as stream:
      settings_yaml = yaml.safe_load(stream)
      self.load_alarm_type(settings_yaml)
      self.load_alarm_repeat(settings_yaml)
      self.load_use_colors(settings_yaml)
      self.load_timers(settings_yaml)

  """Try to load alarm type setting"""
  def load_alarm_type(self, settings_yaml):
    if "alarm_type" in settings_yaml:
      if settings_yaml["alarm_type"] == "beep":
        self._alarm_type = "beep"
      elif settings_yaml["alarm_type"] == "flash":
        self._alarm_type = "flash"

  """Try to load alarm count"""
  def load_alarm_repeat(self, settings_yaml):
    if "alarm_repeat" in settings_yaml:
      if settings_yaml["alarm_repeat"] >= 1:
        self._alarm_repeat = settings_yaml["alarm_repeat"]

  """Try to load color use setting"""
  def load_use_colors(self, settings_yaml):
    if "use_colors" in settings_yaml:
      if settings_yaml["use_colors"]:
        self._use_colors = True
      else:
        self._use_colors = False

  """Try to load timers"""
  def load_timers(self, settings_yaml):
    loaded_timers = []
    if "timers" in settings_yaml:
      for timer in settings_yaml["timers"]:
        if "type" in timer and "duration" in timer:
          if timer["duration"] > 0:
            loaded_timers.append({
              "type": timer["type"],
              "duration": timer["duration"]
            })
    if loaded_timers:
      self._timers = loaded_timers

  """Get timer by id"""
  def get_timer(self, timer_id):
    if timer_id < len(self._timers):
      return self._timers[timer_id]
    else:
      raise IndexError("Timer not found")

  @property
  def selected_config(self):
    return self._selected_config

  @property
  def timers(self):
    return self._timers

  @property
  def use_colors(self):
    return self._use_colors

  @property
  def alarm_repeat(self):
    return self._alarm_repeat

  @property
  def alarm_type(self):
    return self._alarm_type
