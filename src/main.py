import platform
from te2.logger import Logger
from te2.session import Session
from te2.gui import GUI
from te2.ui import UI

from te2.actquene import ActQuene
from te2.world import World
from te2.entity import Entity
from te2.components import Components
from te2.handlers import Handlers

def platformCheck(): 
  """check if system compatible, log info"""
  s = platform.system()
  if s == "Linux": # linux
    Logger.log("Running on Linux. [SUPPORTED: UI]", color="green")
  elif s == "Windows": # windows
    Logger.log("Running on Windows. [SUPPORTED: GUI, UI]", color="green")
  else: # other os
    Logger.log("Running on unknown OS. [NOT SUPPORTED] Things may not work!", color="red")

actQuene1 = ActQuene()

nauvis = World(
  actQuene=actQuene1, 
  name="Nauvis"
)

world.insertCopy(Entity(
  components = [
    Components.positionComponent(x=0, x=0),
    Components.healthComponent(hp=10, maxhp=15)
  ],
  handlers = [
    Handlers.damageHandler
  ]
)

# platformCheck()
# s = platform.system()

# if s == "Windows":
#   ui = ui(Session()) #initalize game gui, assign it a session to control
#   ui.startLoop() #start gui loop, continue past here when it exits
#   Logger.log("Session ended!", color="red")
# elif s == "Linux":
#   ui = UI(Session())
#   ui.startLoop()
#   Logger.log("Session ended!", color="red")