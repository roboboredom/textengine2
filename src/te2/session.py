from te2.logger import Logger
from te2.world import World
from te2.entity import Entity
from te2.components import Components

class Session:
  """
  Session class, contains data for a game session,
  and has methods for manipulating that data.
  """
  def __init__(self):
    Logger.log("Session created.", color="magenta")
    self.loadedWorlds = {}
    self.selectedWorld = None #current selected world in loadedWorlds
  
  def __del__(self):
    Logger.log("Session destroyed.", color="magenta")
  
  def runCommand(self, cmd):
    """run a session command"""
    cmd = cmd.split(" ") #split cmd into pieces by spaces
    
    if cmd[0] == "save":
      if len(cmd) > 1 and len(cmd) <= 2: #command only accepts 2 args
        World.saveWorldFile(self.loadedWorlds[cmd[1]]) #save world to textengine2/game/worlds
        Logger.log("Saved world \"", cmd[1], "\" to worlds folder.", color="green")
      else:
        Logger.log("Invalid amount of arguments.", color="red")
        
    elif cmd[0] == "load":
      if len(cmd) > 1 and len(cmd) <= 2: #command only accepts two arguments   
        world = World.loadWorldFile(cmd[1]) #load world from textengine2/game/worlds/ 
        self.loadedWorlds[world.name] = world #add world to loadedWorlds
        del world
        Logger.log("Loaded world \"", cmd[1], "\" from worlds folder.", color="green")
      else:
        Logger.log("Invalid amount of arguments.", color="red")
    
    elif cmd[0] == "del":
      if len(cmd) > 1 and len(cmd) <= 2: #command only accepts two arguments 
        World.delWorldFile(cmd[1]) #delete world from textengine2/game/worlds/
        Logger.log("Deleted world \"", cmd[1], "\" from worlds folder.", color="green")
      else:
        Logger.log("Invalid amount of arguments.", color="red")
    
    elif cmd[0] == "gen":
      if len(cmd) > 1 and len(cmd) <= 2:
        world = World(cmd[1]) #generate new world
        self.loadedWorlds[world.name] = world #add world (dict key) to loadedWorlds
        del world
      else:
        Logger.log("Invalid amount of arguments.", color="red")
    
    elif cmd[0] == "sel":
      if len(cmd) > 1 and len(cmd) <= 2:
        self.selectedWorld = cmd[1] #set current world
      else:
        Logger.log("Invalid amount of arguments.", color="red")

    elif cmd[0] == "help":
      if len(cmd) == 1:
        Logger.log(
          "\nhelp\n",
          "\tshows this text\n",
          "save <worldname>\n",
          "\tsave world in loadedWorlds to folder \"worlds\"\n",
          "load <worldname>\n",
          "\tload world from folder \"worlds\" to loadedWorlds\n",
          "del <worldname>\n",
          "\tdelete world from folder \"worlds\"\n",
          "gen <worldname>\n",
          "\tgenerate new world, add it to loadedWorlds\n",
          "sel <worldname>\n",
          "\tset selected world (in loadedWorlds)\n",
          "newent <x> <y>\n",
          "\tadd test entity to coords in selected world\n",
          color="green", sep=""
        )
      else:
        Logger.log("Invalid amount of arguments.", color="red")
    
    else:
      Logger.log("No command \"", cmd[0], "\".", color="red")
    
    if self.selectedWorld != None:
      Logger.log("\nselectedWorld: ", self.loadedWorlds[self.selectedWorld].name)
      self.loadedWorlds[self.selectedWorld].print()
