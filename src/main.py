import platform
from te2.logger import Logger
from te2.session import Session
from te2.gui import GUI
from te2.ui import UI

def platformCheck(): 
  """check if system compatible, log info"""
  s = platform.system()
  if s == "Linux": # linux
    Logger.log("Running on Linux. [SUPPORTED: UI]", color="green")
  elif s == "Windows": # windows
    Logger.log("Running on Windows. [SUPPORTED: GUI, UI]", color="green")
  else: # other os
    Logger.log("Running on unknown OS. [NOT SUPPORTED] Things may not work!", color="red")


ui = UI(Session())
ui.startLoop()
Logger.log("Session ended!", color="red")

# platformCheck()
# s = platform.system()

# if s == "Windows":
#   gui = GUI(Session()) #initalize game gui, assign it a session to control
#   gui.startLoop() #start gui loop, continue past here when it exits
#   Logger.log("Session ended!", color="red")
# elif s == "Linux":
#   ui = UI(Session())
#   ui.startLoop()
#   Logger.log("Session ended!", color="red")