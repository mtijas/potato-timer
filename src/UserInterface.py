from curses import wrapper
import curses

class UserInterface:
    def __init__(self, engine):
        self.engine = engine

    def start(self):
        wrapper(self.initUIandBegin)

    def initUIandBegin(self, stdscr):
        self.stdscr = stdscr
        self.buildUserInterface()
        self.drawWelcomeScreen()
        self.listTimers()
        self.startMainLoop()

    def buildUserInterface(self):
        self.content = curses.newwin(10, 40, 0, 0)
        self.sidebar = curses.newwin(10, 20, 0, 40)
        self.content.clear()
        self.sidebar.clear()
        self.content.nodelay(True)
        self.content.border()
        self.sidebar.border()

    def drawWelcomeScreen(self):
        self.content.addstr(1, 1, "Welcome to Tomato Timer!")
        self.content.refresh()

    def listTimers(self):
        self.sidebar.addstr(1, 1, "Current timers")
        self.sidebar.addstr(2, 1, "Type (time):")
        self.sidebar.hline(3, 1, "=", 18)
        i = 4
        for timer in self.engine.getTimers():
            self.sidebar.addstr(i, 1, f"{timer[0]} ({timer[1]})")
            i += 1
        self.sidebar.refresh()

    def startMainLoop(self):
        while True:
            c = self.content.getch()
            if c == ord('q'):
                break
