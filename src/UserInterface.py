from curses import wrapper
import curses
import time

class UserInterface:
    def __init__(self, engine):
        self.engine = engine

    def start(self):
        self.init_curses()
        self.build_user_interface()
        self.draw_welcome_screen()
        try:
            self.main_loop()
        finally:
            self.end_curses()

    def init_curses(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        self.stdscr.keypad(True)

    def end_curses(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def main_loop(self):
        while True:
            c = self.content.getch()
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
           
            self.engine.update()
            self.update_status()
            self.update_sidebar()
            self.refresh_windows()
            time.sleep(0.5)

    def update_status(self):
        if self.engine.running:
            self.status_line.bkgd(' ', curses.color_pair(2))
            self.status_line.addstr(1, 1, "Timer running")
        else:
            self.status_line.bkgd(' ', curses.color_pair(3))
            self.status_line.addstr(1, 1, "Timer stopped")

    def build_user_interface(self):
        self.init_color_pairs()
        self.create_windows()
        self.content.nodelay(True)
        self.status_line.border()
        self.content.border()
        self.sidebar.border()
        self.footer.bkgd(' ', curses.color_pair(8))

    def create_windows(self):
        # calculate window sizes
        height = curses.LINES - 1
        width = curses.COLS - 1
        content_width = round(width * 0.67)
        sidebar_width = width - content_width

        # create windows
        self.content = curses.newwin(height-3, content_width, 3, 0)
        self.sidebar = curses.newwin(height, sidebar_width, 0, content_width)
        self.status_line = curses.newwin(3, content_width, 0, 0)
        self.footer = curses.newwin(1, width, height, 0)

    def draw_welcome_screen(self):
        self.content.addstr(1, 1, "Welcome to Tomato Timer!")
        self.footer.addstr(0, 0, "(s)tart/(s)top, (n)ext timer, (r)eset timer, (q)uit")

    def update_sidebar(self):
        self.sidebar.addstr(1, 1, "Current timers")
        self.sidebar.addstr(2, 1, "Type (time):")
        self.sidebar.hline(3, 1, "=", 18)
        for idx, timer in enumerate(self.engine.timers):
            if idx == self.engine.current_timer_id:
                self.sidebar.addstr(idx+4, 1, f"{timer[0]} ({timer[1]})", curses.color_pair(6))
            else:
                self.sidebar.addstr(idx+4, 1, f"{timer[0]} ({timer[1]})", curses.color_pair(1))

    def init_color_pairs(self):
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(8, curses.COLOR_BLUE, curses.COLOR_BLACK)

    def refresh_windows(self):
        self.status_line.refresh()
        self.content.refresh()
        self.sidebar.refresh()
        self.footer.refresh()
