import copy, json, os, platform

class World:
  
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

  def print(self): #called when object treated as a string
    for y in self.array:
      for x in y:
        if isinstance(x, int):
          print(self.entities[x].symbol, sep="", end="")
        else:
          print(x, sep="", end="")
      print("\n", end="")

  #inserts COPY of input object at it"s stored coords.
  def insertCopy(self, obj):
    clone = copy.deepcopy(obj) #copy it first, so we don"t modify the input obj (reference)
    self.array[clone.y][clone.x] = self.ent_id_count
    self.ent_id_count += 1
    self.entities.append(clone)
  
  #inserts COPY of input object at specific coords
  def insertCopyAt(self, obj, x, y):
    clone = copy.deepcopy(obj)
    clone.x = x
    clone.y = y
    self.array[clone.y][clone.x] = self.ent_id_count
    self.ent_id_count += 1
    self.entities.append(clone)

  #returns value at coords; better than just accessing self.array[][] - coords are backwards due to it"s nesting
  def getVal(self, x, y):
    return self.array[y][x]
  
  #returns entity instance at coords
  def getEntity(self, x, y):
    return self.entities[self.getVal(x, y)]

def saveWorldFile(world): #save world array to file
  clone = copy.deepcopy(world) #copy world so we can modify it"s values just for this function
  
  if platform.system() == "Windows": #diff os filepath formats
    file = open(os.getcwd() + "\\src\\worlds\\" + clone.name + ".json", "w") #create file if not exist, write only
  elif platform.system() == "Linux":
    file = open(os.getcwd() + "/src/worlds/" + clone.name + ".json", "w")

  newlist = []
  for obj in clone.entities: #change objects in list to json
    newlist.append([json.dumps(obj.__class__.__name__), json.dumps(obj.__dict__)])
  clone.entities = newlist

  file.write(json.dumps(clone.__dict__, indent="\t"))
  del clone #we dont need our copy anymore, delete it
  file.close()

def loadWorldFile(name): #load world array from file
  if platform.system() == "Windows": #diff os filepath formats
    file = open(os.getcwd() + "\\src\\worlds\\" + name + ".json", "r") #read only
  elif platform.system() == "Linux":
    file = open(os.getcwd() + "/src/worlds/" + name + ".json", "r")
  
  shell = World(shell=True) #new World instance without instance vars

  with file as f: #load world json
    shell.__dict__ = json.load(f)
  
  newlist = []
  for obj in shell.entities: #change objects in list to instances
    id = json.loads(obj[0]) #new instance of classname
    constructor = globals()[id]
    instance = constructor(shell=True)
    instance.__dict__= json.loads(obj[1])
    newlist.append(instance)
    del instance
    del constructor
  shell.entities = newlist
  
  file.close()
  return shell

def delWorldFile(name): #delete world file
  if platform.system() == "Windows": #diff os filepath formats
    os.remove(os.getcwd() + "\\src\\worlds\\" + name + ".json") #delete file
  elif platform.system() == "Linux":
    os.remove(os.getcwd() + "/src/worlds/" + name + ".json")
  