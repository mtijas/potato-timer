import curses
import time
from curses import wrapper
from datetime import timedelta


class UserInterface:
  def __init__(self, engine, screen):
    self.engine = engine
    self.screen = screen

  """Start user interface"""
  def start(self):
    self.screen.start()
    self.manage_windows()
    self.screen.erase_window("statusline")
    self.screen.erase_window("content")
    self.screen.erase_window("sidebar")
    try:
      self.main_loop()
    finally:
      self.screen.stop()

  """User interface main loop
  # 
  # Handles keystrokes, updates UI and runs timer engine
  """
  def main_loop(self):
    while True:
      c = self.screen.get_char("statusline")
      if c == ord('q'):
        break
      elif c == ord('s'):
        if self.engine.running:
          self.engine.stop_timer()
        else:
          self.engine.start_timer()
      elif c == ord('n'):
        self.engine.next_timer()
        self.engine.reset_timer()
      elif c == ord('r'):
        self.engine.reset_timer()
      elif c == ord('h'):
        self.show_help()
      
      if self.screen.is_resized:
        self.manage_windows()
        self.screen.ack_resize()

      self.engine.update()
      self.handle_alarm()
      self.update_status()
      if self.screen.test_existence("sidebar"):
        self.update_sidebar()
      if self.screen.test_existence("content"):
        self.update_content()
      time.sleep(0.5)

  """Update statusline window"""
  def update_status(self):
    self.screen.erase_window("statusline")
    max_y, max_x = self.screen.get_max_yx("statusline")
    if max_y > 1:
      y = 1
    else:
      y = 0
    if self.engine.running:
      if self.engine.timer_name == "work":
        self.screen.set_background("statusline", " ", 2)
      elif self.engine.timer_name == "short break":
        self.screen.set_background("statusline", " ", 3)
      elif self.engine.timer_name == "long break":
        self.screen.set_background("statusline", " ", 4)
      else:
        self.screen.set_background("statusline", " ", 5)

      status = f"Timer running: {self.engine.timer_name}"
      self.screen.add_centered_str("statusline", y, status)
    else:
      self.screen.set_background("statusline", " ", 1)
      self.screen.add_centered_str("statusline", y, "Timer stopped")
    self.screen.refresh_window("statusline")

  """Update content window"""
  def update_content(self):
    self.screen.erase_window("content")
    max_y, max_x = self.screen.get_max_yx("content")
    elapsed_delta = timedelta(seconds=round(self.engine.time_elapsed))
    duration_delta = timedelta(seconds=self.engine.timer_duration)
    total_delta = timedelta(seconds=round(self.engine.total_time_elapsed))
    working_delta = timedelta(
      seconds=round(self.engine.total_time_working))

    self.screen.add_str("content", 
      1, 2, f"{str(elapsed_delta)}/{str(duration_delta)}")
    if max_y > 12:
      self.screen.add_str("content", 3, 2, f"Completed:")
      self.screen.add_str("content", 
        4, 2, f"Work stints:  {self.engine.work_count}")
      self.screen.add_str("content", 
        5, 2, f"Short breaks: {self.engine.short_count}")
      self.screen.add_str("content", 
        6, 2, f"Long breaks:  {self.engine.long_count}")
      self.screen.add_str("content", 
        8, 2, f"Total time spent:   {str(total_delta)}")
      self.screen.add_str("content", 
        9, 2, f"Time spent working: {str(working_delta)}")

      if self.engine.started_at is not None:
        start_time = time.strftime("%H:%M:%S", self.engine.started_at)
        self.screen.add_str("content", 
          10, 2, f"First timer started at {start_time}")

    self.screen.add_str("content", 0, max_x-10, f'{time.strftime("%H:%M:%S")}')
    self.screen.add_str("content", max_y-1, 2, "(s)tart/(s)top, (h)elp, (q)uit")
    self.screen.refresh_window("content")

  """Update sidebar window"""
  def update_sidebar(self):
    self.screen.erase_window("sidebar")
    self.screen.add_str("sidebar", 1, 2, "Current timers")
    self.screen.add_str("sidebar", 2, 2, "Type (time):")
    self.screen.add_hline("sidebar", 3, 2, "-")
    for idx, timer in enumerate(self.engine.timers):
      if idx == self.engine.current_timer_id:
        self.screen.add_str(
          "sidebar", 
          idx+4, 
          2, 
          f"{timer[0]} ({timer[1]})", self.screen.color_pair(6)
        )
      else:
        self.screen.add_str(
          "sidebar",
          idx+4, 
          2, 
          f"{timer[0]} ({timer[1]})", 
          self.screen.color_pair(1)
        )
    self.screen.refresh_window("sidebar")

  """Handle timer alarms"""
  def handle_alarm(self):
    if self.engine.alarm:
      self.screen.alarm()
      self.engine.ack_alarm()

  """Create, remove and resize windows"""
  def manage_windows(self):
    lines, cols = self.screen.screen_size()
    content_width = cols

    if cols >= 60:
      content_width = round(cols * 0.67)
      sidebar_width = cols - content_width
      self.screen.resize_or_create_window("sidebar", lines, sidebar_width, 0, content_width)
      self.screen.move_window("sidebar", 0, content_width)
    else:
      self.screen.remove_window("sidebar")

    if lines >= 6:
      self.screen.resize_or_create_window("content", lines-3, content_width, 3, 0)
      self.screen.resize_or_create_window("statusline", 3, content_width, 0, 0)
    else:
      self.screen.remove_window("content")
      self.screen.resize_or_create_window("statusline", 1, content_width, 0, 0)

    self.screen.erase_window("statusline")
    self.screen.erase_window("content")
    self.screen.erase_window("sidebar")
    self.screen.set_nodelays()

  """Show help inside content window
  # 
  # Halts timers
  """
  def show_help(self):
    self.engine.stop_timer()
    self.update_status()
    self.screen.erase_window("content")
    self.screen.add_str("content", 1, 2, "Tomato Timer Help")
    self.screen.add_str("content", 3, 2, "s: Start and stop timers")
    self.screen.add_str("content", 4, 2, "n: Next timer (starts from 0)")
    self.screen.add_str("content", 5, 2, "r: Reset current timer")
    self.screen.add_str("content", 6, 2, "h: Show/hide help")
    self.screen.add_str("content", 7, 2, "q: Quit")
    self.screen.refresh_window("content")
    while True:
      c = self.screen.get_char("content")
      if c == ord('h'):
        break
      time.sleep(0.5)
    self.screen.erase_window("content")
