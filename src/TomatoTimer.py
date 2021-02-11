import TimerEngine
import UserInterface
import Screen
import Config

if __name__ == '__main__':
  try:
    config = Config.Config()
  except FileNotFoundError:
    print("Settings file was not found")
    exit()
  
  engine = TimerEngine.TimerEngine(config)
  screen = Screen.Screen(config)
  ui = UserInterface.UserInterface(config, engine, screen)
  ui.start()
