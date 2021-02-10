import curses
from curses import wrapper

class Screen:
  def __init__(self, settings):
    self._settings = settings
    self._windows = {} # Store windows as a dictionary for easy usage
    self._is_resized = False
    self._use_colors = False

  """Initialize curses with defaults"""
  def start(self):
    self.stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
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
    if curses.has_colors and self._settings.use_colors:
      self._use_colors = True
      curses.start_color()
      self._init_color_pairs()


  """Window-specific functions"""

  """Resize window
  #
  # Creates a new window if window does not already exist
  """
  def resize_or_create_window(self, name, height, width, start_y, start_x):
    if self.test_existence(name):
      self._windows[name].resize(height, width)
    else:
      self._windows[name] = curses.newwin(height, width, start_y, start_x)

  """Remove window"""
  def remove_window(self, name):
    if self.test_existence(name):
      del self._windows[name]

  """Move window"""
  def move_window(self, name, y, x):
    self._windows[name].mvwin(y, x)

  """Set window background"""
  def set_background(self, name, chr, color):
    if self._use_colors:
      self._windows[name].bkgd(chr, curses.color_pair(color))

  """Get character from specified curses window"""
  def get_char(self, name):
    c = self._windows[name].getch()
    self.update_status(c)
    return c

  """Clear window and redraw border"""
  def erase_window(self, name):
    if self.test_existence(name):
      self._windows[name].erase()
      y, x = self._windows[name].getmaxyx()
      if y >= 3 and x >= 3:  # borders only for big enough window
        self._windows[name].border()

  """Refresh selected window"""
  def refresh_window(self, name):
    self._windows[name].refresh()

  """Set nodelay attributes to True for all windows"""
  def set_nodelays(self):
    for window in self._windows.values():
      window.nodelay(True)

  """Test for window existence"""
  def test_existence(self, name):
    return name in self._windows

  """Get max y and x"""
  def get_max_yx(self, name):
    return self._windows[name].getmaxyx()

  @property
  def is_resized(self):
    """Getter for is_resized flag"""
    return self._is_resized

  """Acknowledge is_resized flag (situation handled)"""
  def ack_resize(self):
    self._is_resized = False



  """Text management functions"""

  """Add string to screen"""
  def add_str(self, name, y, x, message, color = None):
    max_y, max_x = self._windows[name].getmaxyx()
    max_x -= x*2
    if y < max_y and x < max_x:
      if color is not None and self._use_colors:
        self._windows[name].addnstr(y, x, message, max_x, color)
      else:
        self._windows[name].addnstr(y, x, message, max_x)

  """Add centered string to screen"""
  def add_centered_str(self, name, y, message):
    max_y, max_x = self._windows[name].getmaxyx()
    x = self.calc_start_x(name, message)
    max_x -= x+4 # accommodate borders + padding
    if y < max_y and x < max_x:
      self._windows[name].addnstr(y, x, message, max_x)
  
  """Add horizontal line"""
  def add_hline(self, name, y, x, chr):
    max_y, max_x = self._windows[name].getmaxyx()
    max_x -= x*2 # center the line
    self._windows[name].hline(y, x, chr, max_x)

  """Calculate starting point for horizontally centered text"""
  def calc_start_x(self, name, text):
    y, x = self._windows[name].getmaxyx()
    pos = x // 2 - len(text) // 2
    if pos >= 0:
      return pos
    return 0



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
    if self._settings.alarm_type is "beep":
      curses.beep()
    elif self._settings.alarm_type is "flash":
      curses.flash()

  """Initialize color pairs
  # 
  # 1: White on Black
  # 2: White on Red
  # 3: White on Green
  # 4: White on Blue
  # 5: Black on Yellow
  # 6: Green on Black
  # 8: Blue on Black
  """
  def _init_color_pairs(self):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_BLUE, curses.COLOR_BLACK)