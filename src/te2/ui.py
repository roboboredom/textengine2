from te2.logger import Logger

class UI:
  """UI class, console-based ui for controlling a game session."""
  def __init__(self, session):
    self.session = session #game session to control
  
  def startLoop(self):
    Logger.log("Starting UI loop.", color="red")

    while True:    
      cmd = input("> ")

      if cmd != "quit":
        if cmd.isspace() != True and cmd != "":
          self.session.runCommand(cmd)
                  
        else:
          Logger.log("Nothing Entered!", color="red")
      else:
        Logger.log("UI loop exited by \"quit\" command.", color="red")
        del self
        break
