import argparse
import Config
import Screen
import sys
import TimerEngine
import UserInterface

if __name__ == '__main__':
  parser = argparse.ArgumentParser()

  parser.add_argument('-c', '--config', dest = 'config', help = 'Load a custom configuration file')
  parser.set_defaults(config = None)

  args = parser.parse_args()

  try:
    config = Config.Config(args.config)
    engine = TimerEngine.TimerEngine(config)
    screen = Screen.Screen(config)
    ui = UserInterface.UserInterface(config, engine, screen)
    ui.start()
  except FileNotFoundError:
    print("Settings file was not found")
    exit()
  except SystemExit:
    print("Exiting...")
    exit()
  except:
    print("Unexpected error: ", sys.exc_info()[0])
    exit()
