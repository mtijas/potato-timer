import curses
import time
from curses import wrapper
from datetime import timedelta

class UserInterface:
    def __init__(self, engine):
        self.engine = engine

    def start(self):
        self.init_curses()
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
            elif c == ord('h'):
                self.show_help()
           
            self.engine.update()
            self.handle_alarm()
            self.update_status()
            self.update_sidebar()
            self.update_content()
            self.refresh_windows()
            time.sleep(0.5)

    def update_status(self):
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
            self.status_line.addstr(1, x, status)
        else:
            self.status_line.bkgd(' ', curses.color_pair(1))
            x = self.calc_start_x(self.status_line, "Timer stopped")
            self.status_line.addstr(1, x, "Timer stopped")

    def update_content(self):
        y, x = self.content.getmaxyx()
        self.empty_window(self.content)
        elapsed_delta = timedelta(seconds = round(self.engine.time_elapsed))
        duration_delta = timedelta(seconds = self.engine.timer_duration)
        total_delta = timedelta(seconds = round(self.engine.total_time_elapsed))
        working_delta = timedelta(seconds = round(self.engine.total_time_working))

        self.content.addstr(1, 2, f"Current timer: {self.engine.timer_name}")
        self.content.addstr(2, 2, f"{str(elapsed_delta)}/{str(duration_delta)}")
        self.content.addstr(4, 2, f"Completed:")
        self.content.addstr(5, 2, f"Work stints:  {self.engine.work_count}")
        self.content.addstr(6, 2, f"Short breaks: {self.engine.short_count}")
        self.content.addstr(7, 2, f"Long breaks:  {self.engine.long_count}")
        self.content.addstr(9, 2, f"Total time spent:   {str(total_delta)}")
        self.content.addstr(10, 2, f"Time spent working: {str(working_delta)}")
        
        if self.engine.started_at != None:
            start_time = time.strftime("%H:%M:%S", self.engine.started_at)
            self.content.addstr(11, 2, f"First timer started at {start_time}")
        
        self.content.addstr(0, x-10, f'{time.strftime("%H:%M:%S")}')
        self.content.addstr(y-1, 2, "(s)tart/(s)top, (h)elp, (q)uit")

    def handle_alarm(self):
        if self.engine.alarm:
            curses.beep()
            self.engine.ack_alarm()

    def build_user_interface(self):
        self.init_color_pairs()
        self.create_windows()
        self.content.nodelay(True)
        self.status_line.border()
        self.content.border()
        self.sidebar.border()

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
        self.engine.stop_timer()
        self.update_status()
        self.empty_window(self.content)
        self.content.addstr(1, 2, "Tomato Timer Help")
        self.content.addstr(3, 2, "s: Start and stop timers")
        self.content.addstr(4, 2, "n: Next timer (starts from 0)")
        self.content.addstr(5, 2, "r: Reset current timer")
        self.content.addstr(6, 2, "h: Show/hide help")
        self.content.addstr(7, 2, "q: Quit")
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
        self.content.refresh()
        self.sidebar.refresh()

    def empty_window(self, window):
        window.clear()
        window.border()

    def calc_start_x(self, window, text):
        y, x = window.getmaxyx()
        pos = x // 2 - len(text) // 2
        if pos >= 0:
            return pos
        else:
            return 0

