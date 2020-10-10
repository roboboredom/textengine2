import platform, json
from te2.acts import Acts
from te2.logger import Logger
from te2.session import Session
from te2.gui import GUI
from te2.ui import UI
from te2.actqueue import ActQueue
from te2.world import World
from te2.ecs.entity import Entity
from te2.ecs.component import Components
from te2.ecs.system import System

def platformCheck(): 
  """check if system compatible, log info"""
  s = platform.system()
  if s == "Linux": # linux
    Logger.log("Running on Linux. [SUPPORTED: UI]", color="green")
  elif s == "Windows": # windows
    Logger.log("Running on Windows. [SUPPORTED: GUI, UI]", color="green")
  else: # other os
    Logger.log("Running on unknown OS. [NOT SUPPORTED] Things may not work!", color="red")

world1 = World(name = "Nauvis")