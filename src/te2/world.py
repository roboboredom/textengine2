import copy, json, os, platform, inspect
from te2.actqueue import ActQueue

class World:
  """
  class for a world, containing entities and tiles
  set shell=True to skip __init__ (no instance vars)
  """
  xLenMax = 32 #world size caps
  yLenMax = 32
  
  def __init__(self, name=None, xlen=8, ylen=8, shell=False):
    if not shell: #for deserialization, True = don"t instantiate any variables
      self.name = name
      self.xlen = xlen
      self.ylen = ylen
      
      self.tiles = [] 
      for _y in range(0, self.ylen): #create default tiles of "." from dimensions
        row = []
        for _x in range(0, self.xlen):
          row.append(".")
        self.tiles.append(row)
      
      self.entIdCount = 0 #each entity has a unique id that stays the same between loads
      self.entities = []

      self.queue = ActQueue(world=self)

  def print(self):
    """print world to console"""
    print("id count:", self.ent_id_count)
    for y in self.tiles:
      for x in y:
        if isinstance(x, list):
          print(self.entities[x[-1]], sep="", end="") #if entities on tile, display top entity on tile
        else:
          print(x, sep="", end="")
      print("\n", end="")

  def insertAt(self, obj):
    """Insert entity at the coords in it's positionComponent."""
    clone = copy.deepcopy(obj) #copy it first, so we don't modify the input obj (reference)

    coords = clone.components["positionComponent"]["coords"]
    x = coords[0]
    y = coords[1]
    
    if isinstance(self.tiles[y][x], list): #allow entity stacking
      self.tiles[y][x].append(self.entIdCount)
    else:
      self.tiles[y][x] = [self.tiles[y][x], self.entIdCount]
    
    clone.id = self.entIdCount
    self.entIdCount += 1
    self.entities.append(clone)
  
  def insert(self, obj):
    """Insert an entity into the world's entities, but do not place it in the world."""
    clone = copy.deepcopy(obj) #copy it first, so we don't modify the input obj (reference)

    clone.id = self.entIdCount
    self.entIdCount += 1
    self.entities.append(clone)

  def setTile(self, x, y, char):
    if isinstance(self.tiles[y][x], list):
      self.tiles[y][x][0] = char
    else:
      self.tiles[y][x] = char

  def getTile(self, x, y): # Always use instead of accessing self.tiles directly!
    """Return tile value at coords."""
    if isinstance(self.tiles[y][x], list):
      return self.tiles[y][x][0]
    else:
      return self.tiles[y][x]
  
  def getEntitiesAt(self, x, y):
    """Return any entities at coords."""
    if isinstance(self.tiles[y][x], list):
      ents = []
      for ID in self.tiles[y][x][1:]:
        ents.append(self.entities[ID])
      return ents
    else:
      return None

  @staticmethod
  def saveWorldFile(world):
    """save a world to a world file"""
    clone = copy.deepcopy(world) #copy world so we can modify it"s values just for this function
    
    if platform.system() == "Windows": #diff os filepath formats
      worldFile = open(os.getcwd() + "\\game\\worlds\\" + clone.name + ".te2wrld", "w") #create file if not exist, write only
    elif platform.system() == "Linux":
      worldFile = open(os.getcwd() + "/game/worlds/" + clone.name + ".te2wrld", "w")

    newlist = []
    for obj in clone.entities: #change objects in list to json
      newlist.append([json.dumps(obj.__class__.__name__), json.dumps(obj.__dict__)])
    clone.entities = newlist

    worldFile.write(json.dumps(clone.__dict__, indent="\t"))
    
    del clone #we dont need our copy anymore, delete it
    worldFile.close()

  @staticmethod
  def loadWorldFile(name):
    """load a world file, return it"""
    if platform.system() == "Windows": #diff os filepath formats
      worldFile = open(os.getcwd() + "\\game\\worlds\\" + name + ".te2wrld", "r") #read only
    elif platform.system() == "Linux":
      worldFile = open(os.getcwd() + "/game/worlds/" + name + ".te2wrld", "r")
    
    shell = World(shell=True) #new World instance without instance vars

    with worldFile as f: #load world json
      shell.__dict__ = json.load(f)
    
    newlist = []
    for obj in shell.entities: #change objects in list to instances
      classname = json.loads(obj[0]) #loaded class must be BaseEntity or inherit from BaseEntity
      
      instance = inspect.stack()[1][0].f_globals[classname](shell=True) #get globals of main.py
      
      instance.__dict__= json.loads(obj[1])

      newlist.append(instance)
      del instance
    shell.entities = newlist
    
    worldFile.close()
    return shell

  @staticmethod
  def delWorldFile(name):
    """delete a world file"""
    if platform.system() == "Windows": #diff os filepath formats
      os.remove(os.getcwd() + "\\game\\worlds\\" + name + ".te2wrld") #delete file
    elif platform.system() == "Linux":
      os.remove(os.getcwd() + "/game/worlds/" + name + ".te2wrld")