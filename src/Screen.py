import curses
import time
import math

class Screen:
  def __init__(self, config):
    self._config = config
    self._windows = {} # Store windows as a dictionary for easy usage
    self._is_resized = False
    self._use_colors = False

  """Initialize curses with defaults"""
  def start(self):
    self.stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    self.try_colors()
    self.stdscr.keypad(True)
    curses.setsyx(-1, -1)

  """Revert terminal to original state"""
  def stop(self):
    curses.nocbreak()
    self.stdscr.keypad(False)
    curses.echo()
    curses.endwin()

  """Try to use colors"""
  def try_colors(self):
    if curses.has_colors and self._config.use_colors:
      self._use_colors = True
      curses.start_color()
      self._init_colors()


  """Window-specific functions"""

  """Resize window
  #
  # Creates a new window if window does not already exist
  """
  def resize_or_create_window(self, win, height, width, start_y, start_x):
    if self.test_existence(win):
      self._windows[win].resize(height, width)
    else:
      self._windows[win] = curses.newwin(height, width, start_y, start_x)

  """Remove window"""
  def remove_window(self, win):
    if self.test_existence(win):
      del self._windows[win]

  """Move window"""
  def move_window(self, win, y, x):
    self._windows[win].mvwin(y, x)

  """Set window background"""
  def set_background(self, win, chr, color):
    if self._use_colors:
      self._windows[win].bkgd(chr, curses.color_pair(color))

  """Get character from specified curses window"""
  def get_char(self, win):
    c = self._windows[win].getch()
    self.update_status(c)
    return c

  """Clear window and redraw border"""
  def erase_window(self, win):
    if self.test_existence(win):
      self._windows[win].erase()
      y, x = self._windows[win].getmaxyx()
      if y >= 3 and x >= 3:  # borders only for big enough window
        self._windows[win].border()

  """Refresh selected window"""
  def refresh_window(self, win):
    self._windows[win].refresh()

  """Set nodelay attributes to True for all windows"""
  def set_nodelays(self):
    for window in self._windows.values():
      window.nodelay(True)

  """Test for window existence"""
  def test_existence(self, win):
    return win in self._windows

  """Get max y and x"""
  def get_max_yx(self, win):
    return self._windows[win].getmaxyx()

  @property
  def is_resized(self):
    """Getter for is_resized flag"""
    return self._is_resized

  """Acknowledge is_resized flag (situation handled)"""
  def ack_resize(self):
    self._is_resized = False



  """Text management functions"""

  """Add string to screen"""
  def add_str(self, win, y, x, message, color = None):
    max_y, max_x = self._windows[win].getmaxyx()
    max_len = max_x-x-1 # accommodate borders + padding
    if y < max_y and x < max_x and max_len > 0:
      if color is not None and self._use_colors:
        self._windows[win].addnstr(y, x, message, max_len, color)
      else:
        self._windows[win].addnstr(y, x, message, max_len)

  """Add centered string to screen"""
  def add_centered_str(self, win, y, message, color = None):
    x = self.calc_start_x(win, message)
    self.add_str(win, y, x, message, color)
  
  """Add horizontal line"""
  def add_hline(self, win, y, x, chr):
    max_y, max_x = self._windows[win].getmaxyx()
    max_len = max_x-x-2 # accommodate borders + padding
    if y < max_y and x < max_x:
      self._windows[win].hline(y, x, chr, max_len)

  """Calculate starting point for horizontally centered text"""
  def calc_start_x(self, win, text):
    y, x = self._windows[win].getmaxyx()
    pos = x // 2 - len(text) // 2
    if pos >= 0:
      return pos
    return 0

  """Draw horizontal bar"""
  def draw_progress_bar(self, win, y, x, total_len, percent, color = None):
    needed_chars = round(total_len * percent)
    if needed_chars > total_len:
      needed_chars = total_len
    elif needed_chars < 0:
      needed_chars = 0
    
    bar = ""
    for i in range(0, needed_chars):
      bar += "#"

    self.add_str(win, y, x, bar, color)



  """Helpers"""

  """Update screen status"""
  def update_status(self, c):
    if c == curses.KEY_RESIZE:
      self._is_resized = True

  """Get screen size"""
  def screen_size(self):
    curses.update_lines_cols()
    return curses.LINES, curses.COLS

  """Returns curses color pair
  # 
  # Returns NoneType if colors are not in use
  """
  def color_pair(self, i):
    if self._use_colors:
      return curses.color_pair(i)
    else:
      return None

  """Alarm"""
  def alarm(self):
    for i in range(self._config.alarm_repeat):
      if self._config.alarm_type == "beep":
        curses.beep()
      elif self._config.alarm_type == "flash":
        curses.flash()
      time.sleep(0.5)

  """Initialize colors"""
  def _init_colors(self):
    curses.use_default_colors()

    if curses.can_change_color() and not self._config.prefer_terminal_colors:
      curses.init_color(curses.COLOR_RED, 1000, 300, 300)
      curses.init_color(curses.COLOR_GREEN, 500, 1000, 300)
      curses.init_color(curses.COLOR_BLUE, 300, 700, 1000)
      curses.init_color(curses.COLOR_YELLOW, 1000, 750, 0)

    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_GREEN, -1)
    curses.init_pair(4, curses.COLOR_BLUE, -1)
    curses.init_pair(5, curses.COLOR_YELLOW, -1)
