import TimerEngine
import UserInterface
import Screen
import Settings

if __name__ == '__main__':
  settings = Settings.Settings()
  engine = TimerEngine.TimerEngine(settings)
  screen = Screen.Screen(settings)
  ui = UserInterface.UserInterface(settings, engine, screen)
  ui.start()
