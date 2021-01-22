"""
Primary command line interface for TomatoTimerCli

Author: Markus Ijäs
"""
class UserInterface:
  tomatoTimer = None

  def __init__(self, timer) -> None:
    tomatoTimer = timer

  def start(self):
    self.printStatus()

  def printStatus(self):
    print("##TomatoTimerCli##")
    print("# Status: {1}").format(self.tomatoTimer.status())
    print("# Time remaining: {1}/{2}").format(self.tomatoTimer.getRemainingTime(), self.tomatoTimer.getDuration())