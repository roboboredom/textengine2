from logger import Logger

class UI:
  """UI class, console-based ui for controlling a game session."""
  def __init__(self, session):
    self.session = session #game session to control
  
  def startLoop(self):
    Logger.log("Starting UI loop.", color="red")
    
    while True:      
      cmd = input("> ").lower()

      if cmd.isspace() != True and cmd != "":
        self.session.runCommand(cmd)
      else:
        Logger.log("Nothing Entered!", color="red")