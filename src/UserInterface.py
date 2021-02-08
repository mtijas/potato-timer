import curses
import time
from curses import wrapper
from datetime import timedelta

class UserInterface:
    def __init__(self, engine):
        self.engine = engine

    def start(self):
        self.init_curses()
        curses.setsyx(-1, -1) # Set cursor away and leaveok True
        self.build_user_interface()
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
            c = self.status_line.getch()
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
            elif c == curses.KEY_RESIZE:
                self.resize_windows()
           
            self.engine.update()
            self.handle_alarm()
            self.update_status()
            if self.sidebar is not None:
                self.update_sidebar()
            if self.content is not None:
                self.update_content()
            self.refresh_windows()
            time.sleep(0.5)

    def update_status(self):
        max_y, max_x = self.status_line.getmaxyx()
        if max_y > 1:
            y = 1
        else:
            y = 0
        self.empty_window(self.status_line)
        if self.engine.running:
            if self.engine.timer_name == "work":
                self.status_line.bkgd(' ', curses.color_pair(2))
            elif self.engine.timer_name == "short break":
                self.status_line.bkgd(' ', curses.color_pair(3))
            elif self.engine.timer_name == "long break":
                self.status_line.bkgd(' ', curses.color_pair(4))
            else:
                self.status_line.bkgd(' ', curses.color_pair(5))

            status = f"Timer running: {self.engine.timer_name}"
            x = self.calc_start_x(self.status_line, status)
            self.status_line.addstr(y, x, status)
        else:
            self.status_line.bkgd(' ', curses.color_pair(1))
            x = self.calc_start_x(self.status_line, "Timer stopped")
            self.status_line.addstr(y, x, "Timer stopped")

    def update_content(self):
        y, x = self.content.getmaxyx()
        max_x = x-4
        self.empty_window(self.content)
        elapsed_delta = timedelta(seconds = round(self.engine.time_elapsed))
        duration_delta = timedelta(seconds = self.engine.timer_duration)
        total_delta = timedelta(seconds = round(self.engine.total_time_elapsed))
        working_delta = timedelta(seconds = round(self.engine.total_time_working))

        self.content.addnstr(1, 2, f"{str(elapsed_delta)}/{str(duration_delta)}", max_x)
        if y > 12:
            self.content.addnstr(3, 2, f"Completed:", max_x)
            self.content.addnstr(4, 2, f"Work stints:  {self.engine.work_count}", max_x)
            self.content.addnstr(5, 2, f"Short breaks: {self.engine.short_count}", max_x)
            self.content.addnstr(6, 2, f"Long breaks:  {self.engine.long_count}", max_x)
            self.content.addnstr(8, 2, f"Total time spent:   {str(total_delta)}", max_x)
            self.content.addnstr(9, 2, f"Time spent working: {str(working_delta)}", max_x)
        
            if self.engine.started_at != None:
                start_time = time.strftime("%H:%M:%S", self.engine.started_at)
                self.content.addnstr(10, 2, f"First timer started at {start_time}", max_x)
        
        self.content.addnstr(0, x-10, f'{time.strftime("%H:%M:%S")}', max_x)
        self.content.addnstr(y-1, 2, "(s)tart/(s)top, (h)elp, (q)uit", max_x)

    def handle_alarm(self):
        if self.engine.alarm:
            curses.beep()
            self.engine.ack_alarm()

    def build_user_interface(self):
        self.init_color_pairs()
        self.create_windows()
        self.set_no_delays()
        self.empty_window(self.status_line)
        self.empty_window(self.content)
        self.empty_window(self.sidebar)

    def create_windows(self):
        content_width = curses.COLS
        if curses.COLS >= 60:
            content_width = round(curses.COLS * 0.67)
            sidebar_width = curses.COLS - content_width
            self.sidebar = curses.newwin(curses.LINES, sidebar_width, 0, content_width)
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
                self.sidebar = curses.newwin(curses.LINES, sidebar_width, 0, content_width)
            self.empty_window(self.sidebar)
        else:
            self.sidebar = None

        if curses.LINES >= 6:
            if self.content is not None:
                self.content.resize(curses.LINES-3, content_width)
            else:
                self.content = curses.newwin(curses.LINES-3, content_width, 3, 0)
            self.status_line.resize(3, content_width)
        else:
            self.content = None
            self.status_line.resize(1, content_width)
                
        self.set_no_delays()

    def update_sidebar(self):
        self.sidebar.addstr(1, 2, "Current timers")
        self.sidebar.addstr(2, 2, "Type (time):")
        self.sidebar.hline(3, 2, "-", 14)
        for idx, timer in enumerate(self.engine.timers):
            if idx == self.engine.current_timer_id:
                self.sidebar.addstr(idx+4, 2, f"{timer[0]} ({timer[1]})", curses.color_pair(6))
            else:
                self.sidebar.addstr(idx+4, 2, f"{timer[0]} ({timer[1]})", curses.color_pair(1))

    def show_help(self):
        if self.content is None:
            return
        y, x = self.content.getmaxyx()
        max_x = x-4
        self.engine.stop_timer()
        self.update_status()
        self.empty_window(self.content)
        self.content.addnstr(1, 2, "Tomato Timer Help", max_x)
        self.content.addnstr(3, 2, "s: Start and stop timers", max_x)
        self.content.addnstr(4, 2, "n: Next timer (starts from 0)", max_x)
        self.content.addnstr(5, 2, "r: Reset current timer", max_x)
        self.content.addnstr(6, 2, "h: Show/hide help", max_x)
        self.content.addnstr(7, 2, "q: Quit", max_x)
        self.refresh_windows()
        while True:
            c = self.content.getch()
            if c == ord('h'):
                break
            time.sleep(0.5)

    def init_color_pairs(self):
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(8, curses.COLOR_BLUE, curses.COLOR_BLACK)

    def refresh_windows(self):
        self.status_line.refresh()
        if self.content:
            self.content.refresh()
        if self.sidebar:
            self.sidebar.refresh()

    def empty_window(self, window):
        if window is None:
            return
        window.clear()
        y, x = window.getmaxyx()
        if y >= 3:
            window.border()

    def calc_start_x(self, window, text):
        y, x = window.getmaxyx()
        pos = x // 2 - len(text) // 2
        if pos >= 0:
            return pos
        else:
            return 0

    def set_no_delays(self):
        if self.content is not None:
            self.content.nodelay(True)
        if self.status_line is not None:
            self.status_line.nodelay(True)
        if self.sidebar is not None:
            self.sidebar.nodelay(True)
