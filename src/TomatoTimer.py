import TimerEngine
import UserInterface

if __name__ == '__main__':
  engine = TimerEngine.TimerEngine()
  ui = UserInterface.UserInterface(engine)
  ui.start()
