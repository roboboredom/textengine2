"""world class and save/load functions"""
import copy, json, os, platform, inspect

class World:
  """
  class for a world, containing entities and tiles
  set shell=True to skip __init__ (no instance vars)
  """
  xlen_max = 32 #world size caps
  ylen_max = 32
  
  def __init__(self, name=None, xlen=8, ylen=8, shell=False):
    if not shell: #for deserialization, True = don"t instantiate any variables
      self.name = name
      
      if xlen < 0 or xlen > World.xlen_max: #check for bad map dimensions
        raise Exception("[cannot create world \""+self.name+"\", xlen too big]")
      if ylen < 0 or ylen > World.ylen_max:
        raise Exception("[cannot create world \""+self.name+"\", ylen too big]")
      self.xlen = xlen
      self.ylen = ylen
      
      self.array = [] 
      for y in range(0, self.ylen): #create default array of "." from dimensions
        row = []
        for x in range(0, self.xlen):
          row.append(".")
        self.array.append(row)
      
      self.ent_id_count = 0 #each entity has a unique id that stays the same between loads
      self.entities = []

  def print(self):
    """print world to console"""
    for y in self.array:
      for x in y:
        if isinstance(x, int):
          print(self.entities[x].symbol, sep="", end="")
        else:
          print(x, sep="", end="")
      print("\n", end="")

  def insertCopy(self, obj):
    """insert copy of object @ it's stored coords"""
    clone = copy.deepcopy(obj) #copy it first, so we don"t modify the input obj (reference)
    self.array[clone.y][clone.x] = self.ent_id_count
    self.ent_id_count += 1
    self.entities.append(clone)
  
  def insertCopyAt(self, obj, x, y):
    """insert copy of object @ coords"""
    clone = copy.deepcopy(obj)
    clone.x = x
    clone.y = y
    self.array[clone.y][clone.x] = self.ent_id_count
    self.ent_id_count += 1
    self.entities.append(clone)

  def getSymbol(self, x, y): #better than just accessing self.array[][] - coords are backwards due to it's nesting
    """returns symbol @ coords"""
    return self.array[y][x]
  
  def getEntity(self, x, y):
    """returns entity instance @ coords"""
    return self.entities[self.getSymbol(x, y)]

def saveWorldFile(world):
  """save a world to a world file"""
  clone = copy.deepcopy(world) #copy world so we can modify it"s values just for this function
  
  if platform.system() == "Windows": #diff os filepath formats
    file = open(os.getcwd() + "\\game\\worlds\\" + clone.name + ".json", "w") #create file if not exist, write only
  elif platform.system() == "Linux":
    file = open(os.getcwd() + "/game/worlds/" + clone.name + ".json", "w")

  newlist = []
  for obj in clone.entities: #change objects in list to json
    newlist.append([json.dumps(obj.__class__.__name__), json.dumps(obj.__dict__)])
  clone.entities = newlist

  file.write(json.dumps(clone.__dict__, indent="\t"))
  
  del clone #we dont need our copy anymore, delete it
  file.close()

def loadWorldFile(name):
  """load a world file, return it"""
  if platform.system() == "Windows": #diff os filepath formats
    file = open(os.getcwd() + "\\game\\worlds\\" + name + ".json", "r") #read only
  elif platform.system() == "Linux":
    file = open(os.getcwd() + "/game/worlds/" + name + ".json", "r")
  
  shell = World(shell=True) #new World instance without instance vars

  with file as f: #load world json
    shell.__dict__ = json.load(f)
  
  newlist = []
  for obj in shell.entities: #change objects in list to instances
    classname = json.loads(obj[0]) #loaded class must be BaseEntity or inherit from BaseEntity
    
    instance = inspect.stack()[1][0].f_globals[classname](shell=True) #get globals of main.py
    
    instance.__dict__= json.loads(obj[1])

    newlist.append(instance)
    del instance
  shell.entities = newlist
  
  file.close()
  return shell

def delWorldFile(name):
  """delete a world file"""
  if platform.system() == "Windows": #diff os filepath formats
    os.remove(os.getcwd() + "\\game\\worlds\\" + name + ".json") #delete file
  elif platform.system() == "Linux":
    os.remove(os.getcwd() + "/game/worlds/" + name + ".json")