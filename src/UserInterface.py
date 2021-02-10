import curses
import time
from curses import wrapper
from datetime import timedelta


class UserInterface:
  def __init__(self, engine, screen):
    self.engine = engine
    self.screen = screen

  def start(self):
    self.screen.start()
    self.build_user_interface()
    try:
      self.main_loop()
    finally:
      self.screen.stop()

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
      # @TODO: Implement proper resize callback
      #elif c == curses.KEY_RESIZE:
      #  self.resize_windows()

      self.engine.update()
      self.handle_alarm()
      self.update_status()
      if self.screen.test_existence("sidebar"):
        self.update_sidebar()
      if self.screen.test_existence("content"):
        self.update_content()
      time.sleep(0.5)

  def update_status(self):
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

  def update_content(self):
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

  def update_sidebar(self):
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

  def handle_alarm(self):
    if self.engine.alarm:
      self.screen.alarm()
      self.engine.ack_alarm()

  def build_user_interface(self):
    self.create_windows()
    self.screen.set_nodelays()
    self.screen.clear_window("statusline")
    self.screen.clear_window("content")
    self.screen.clear_window("sidebar")

  def create_windows(self):
    content_width = curses.COLS
    if curses.COLS >= 60:
      content_width = round(curses.COLS * 0.67)
      sidebar_width = curses.COLS - content_width
      self.sidebar = curses.newwin(
        curses.LINES, sidebar_width, 0, content_width)
    else:
      self.sidebar = None

    if curses.LINES >= 6:
      self.content = curses.newwin(curses.LINES-3, content_width, 3, 0)
      self.status_line = curses.newwin(3, content_width, 0, 0)
    else:
      self.content = None
      self.status_line = curses.newwin(1, content_width, 0, 0)

  def resize_windows(self):
    curses.update_lines_cols()
    content_width = curses.COLS
    if curses.COLS >= 60:
      content_width = round(curses.COLS * 0.67)
      sidebar_width = curses.COLS - content_width
      if self.sidebar is not None:
        self.sidebar.resize(curses.LINES, sidebar_width)
        self.sidebar.mvwin(0, content_width)
      else:
        self.sidebar = curses.newwin(
          curses.LINES, sidebar_width, 0, content_width)
      self.empty_window(self.sidebar)
    else:
      self.sidebar = None

    if curses.LINES >= 6:
      if self.content is not None:
        self.content.resize(curses.LINES-3, content_width)
      else:
        self.content = curses.newwin(
          curses.LINES-3, content_width, 3, 0)
      self.status_line.resize(3, content_width)
    else:
      self.content = None
      self.status_line.resize(1, content_width)

    self.set_no_delays()

  def show_help(self):
    self.engine.stop_timer()
    self.update_status()
    self.screen.empty_window("content")
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
