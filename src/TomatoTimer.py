import TimerEngine
import UserInterface
import Screen

if __name__ == '__main__':
  engine = TimerEngine.TimerEngine()
  screen = Screen.Screen()
  ui = UserInterface.UserInterface(engine, screen)
  ui.start()
