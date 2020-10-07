import platform, json
from te2.acts import Acts
from te2.logger import Logger
# from te2.session import Session
# from te2.gui import GUI
# from te2.ui import UI

from te2.actqueue import ActQueue
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

world1 = World(name = "Nauvis")

world1.insert(Entity())

world1.insertAt(
  Entity(
    components = [
      Components.positionComponent(
        coords = (1, 1), 
        canShareTile = True
      ),
      Components.healthComponent(
        hp = 10, 
        maxhp = 15
      )
    ],
    handlers = [
      Handlers.damageHandler
    ]
  )
)

world1.queue.addAct(
  Acts.damageAct(
    actorId = 0, 
    doneToCoords = (1, 1), 
    dmg = 2
  )
)
world1.queue.doEntityLoop()

print(world1.queue.queue)