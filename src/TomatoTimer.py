import TimerEngine
import UserInterface
import Screen
import Config
import argparse

if __name__ == '__main__':
  parser = argparse.ArgumentParser()

  parser.add_argument('-c', '--config', dest = 'config', help = 'Load a custom configuration file')
  parser.set_defaults(config = None)

  args = parser.parse_args()

  try:
    config = Config.Config(args.config)
  except FileNotFoundError:
    print("Settings file was not found")
    exit()
  
  engine = TimerEngine.TimerEngine(config)
  screen = Screen.Screen(config)
  ui = UserInterface.UserInterface(config, engine, screen)
  ui.start()
