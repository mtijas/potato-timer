import curses
from curses import wrapper

class Screen:
  def __init__(self):
    # Store windows as a dictionary for easy usage
    self._windows = {}

  """Initialize curses with defaults"""
  def start(self):
    self.stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    self.init_color_pairs()
    self.stdscr.keypad(True)
    curses.setsyx(-1, -1)

  """Revert terminal to original state"""
  def stop(self):
    curses.nocbreak()
    self.stdscr.keypad(False)
    curses.echo()
    curses.endwin()

  """Add string to screen"""
  def add_str(self, name, y, x, message):
    max_y, max_x = self._windows[name].getmaxyx()
    max_x -= x*2
    self._windows[name].addnstr(y, x, message, max_x)

  """Add centered string to screen"""
  def add_centered_str(self, name, y, message):
    max_y, max_x = self._windows[name].getmaxyx()
    x = self.calc_start_x(name, message)
    max_x -= x+4 # accommodate borders + padding
    self._windows[name].addnstr(y, x, message, max_x)
  
  """Add horizontal line"""
  def add_hline(self, name, y, x, chr):
    max_y, max_x = self._windows[name].getmaxyx()
    max_x -= x*2 # center the line
    self._windows[name].hline(y, x, chr, max_x)

  """Set window background"""
  def set_background(self, name, chr, color):
    self._windows[name].bkgd(chr, curses.color_pair(color))

  """Get character from specified curses window"""
  def get_char(self, name):
    return self._windows[name].getch()

  """Clear window and redraw border"""
  def clear_window(self, name):
    self._windows[name].clear()
    y, x = self._windows[name].getmaxyx()
    if y >= 3 and x >= 3:  # borders only for big enough window
      self._windows[name].border()

  """Calculate starting point for horizontally centered text"""
  def calc_start_x(self, name, text):
    y, x = self._windows[name].getmaxyx()
    pos = x // 2 - len(text) // 2
    if pos >= 0:
      return pos
    return 0

  """Refresh selected window"""
  def refresh_window(self, name):
    self._windows[name].refresh()

  """Set nodelay attributes to True for all windows"""
  def set_nodelays(self):
    for window in self._windows:
      window.nodelay(True)

  """Test for window existence"""
  def test_existence(self, name):
    if self._windows[name] is not None:
      return True
    return False

  """Returns curses color pair"""
  def color_pair(self, i):
    return curses.color_pair(i)

  """Get max y and x"""
  def get_max_yx(self, name):
    return self._windows[name].getmaxyx()

  """Alarm"""
  def alarm(self):
    curses.beep()

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
  def init_color_pairs(self):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_BLUE, curses.COLOR_BLACK)