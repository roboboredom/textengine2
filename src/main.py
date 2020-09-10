import random, copy, json, debug, os

# ============================ CLASS DEFINITION =================================
class BaseEntity: #base class for any entity in the world

  def __init__(self, name=None, symbol=None, x=0, y=0, shell=False): #called on instance creation
    if not shell:
      self.name = name
      self.symbol = symbol #symbol representing this object
      self.x = x
      self.y = y

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
          r = random.randint(0,3)
          if r == 3:
            row.append(".")
          elif r == 2:
            row.append("~")
          elif r == 1:
            row.append("v")
          else:
            row.append("w")
        self.array.append(row)
      
      self.ent_id_count = 0 #each entity has a unique id that stays the same between loads
      self.entities = []

  def print(self): #called when object treated as a string
    print(debug.clrcodes.fg.BLUE, end="")
    for y in self.array:
      for x in y:
        if isinstance(x, int):
          print(self.entities[x].symbol, sep="", end="")
        else:
          print(x, sep="", end="")
      print("\n", end="")
    print(debug.clrcodes.fg.WHITE, end="")

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

# ============================ FUNCTION DEFINITIONS ============================
def saveWorldFile(world): #save world array to file
  clone = copy.deepcopy(world) #copy world so we can modify it"s values just for this function
  
  if debug.platformName() == "Windows": #diff os filepath formats
    file = open(os.getcwd() + "\\src\\worlds\\" + clone.name + ".json", "w") #create file if not exist, write only
  elif debug.platformName() == "Linux":
    file = open(os.getcwd() + "/src/worlds/" + clone.name + ".json", "w")

  newlist = []
  for obj in clone.entities: #change objects in list to json
    newlist.append([json.dumps(obj.__class__.__name__), json.dumps(obj.__dict__)])
  clone.entities = newlist

  file.write(json.dumps(clone.__dict__, indent="\t"))
  del clone #we dont need our copy anymore, delete it
  file.close()

def loadWorldFile(name): #load world array from file
  if debug.platformName() == "Windows": #diff os filepath formats
    file = open(os.getcwd() + "\\src\\worlds\\" + name + ".json", "r") #read only
  elif debug.platformName() == "Linux":
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
  if debug.platformName() == "Windows": #diff os filepath formats
    os.remove(os.getcwd() + "\\src\\worlds\\" + name + ".json") #delete file
  elif debug.platformName() == "Linux":
    os.remove(os.getcwd() + "/src/worlds/" + name + ".json")
  
# ============================ MAIN ============================================
debug.platformCheck() #check if platform/os compatible
print(debug.clrcodes.fg.GREEN, ">>>>>> textengine2 || by dawson gray <<<<<< \nType \"help\" for a list of commands.\n", debug.clrcodes.fg.WHITE, sep="")

#template instances
t_rock = BaseEntity("Rock", "#")
t_bush = BaseEntity("Bush", "%")

curWorld = None
while True: #mainloop
  cmd = input("> ")

  if cmd != "" and cmd.isspace() == False: #test if input is only whitespace or empty
    cmd = cmd.split() #split cmd by spaces into list of words

    if cmd[0] == "save":
      if len(cmd) > 1 and len(cmd) <= 2: #command only accepts 2 args
        try:
          curWorld = World(cmd[1])
          
          curWorld.insertCopyAt(t_rock, 2, 3) #EXAMPLE FILLER ENTITIES
          curWorld.insertCopyAt(t_rock, 1, 1) 
          curWorld.insertCopyAt(t_bush, 4, 2)
          
          saveWorldFile(curWorld) #save world to textengine2/src/worlds
          
          print(debug.clrcodes.fg.GREEN + "Saved world \"" + cmd[1] + "\" to worlds folder." + debug.clrcodes.fg.WHITE)
        except:
          print(debug.clrcodes.fg.RED + "World name \"" + cmd[1] + "\" cannot be used as filename." + debug.clrcodes.fg.WHITE)
      else:
        print(debug.clrcodes.fg.RED + "Invalid amount of arguments." + debug.clrcodes.fg.WHITE)
        
    elif cmd[0] == "load":
      if len(cmd) > 1 and len(cmd) <= 2: #command only accepts two arguments 
        try:
          curWorld = loadWorldFile(cmd[1]) #load world from textengine2/src/worlds/ 
          
          print(debug.clrcodes.fg.GREEN + "Loaded world \"" + cmd[1] + "\" from worlds folder." + debug.clrcodes.fg.WHITE)
        except:
          print(debug.clrcodes.fg.RED + "No world named \"" + cmd[1] + "\" saved." + debug.clrcodes.fg.WHITE)
      else:
        print(debug.clrcodes.fg.RED + "Invalid amount of arguments." + debug.clrcodes.fg.WHITE)
    
    elif cmd[0] == "del":
      if len(cmd) > 1 and len(cmd) <= 2: #command only accepts two arguments 
        try:
          delWorldFile(cmd[1]) #load world from textengine2/src/worlds/
          
          print(debug.clrcodes.fg.GREEN + "Deleted world \"" + cmd[1] + "\" from worlds folder." + debug.clrcodes.fg.WHITE)
        except:
          print(debug.clrcodes.fg.RED + "No world named \"" + cmd[1] + "\" saved." + debug.clrcodes.fg.WHITE)
      else:
        print(debug.clrcodes.fg.RED + "Invalid amount of arguments." + debug.clrcodes.fg.WHITE)
    
    elif cmd[0] == "help":
      if len(cmd) == 1:
        print(debug.clrcodes.fg.GREEN +
              "save <worldname>\n" +
              "load <worldname>\n" +
              "del <worldname>\n" +
              "help" + debug.clrcodes.fg.WHITE)
      else:
        print(debug.clrcodes.fg.RED + "Invalid amount of arguments." + debug.clrcodes.fg.WHITE)

    else:
      print(debug.clrcodes.fg.RED + "Invalid command." + debug.clrcodes.fg.WHITE)
  else: 
    print(debug.clrcodes.fg.RED + "No command entered." + debug.clrcodes.fg.WHITE)
    
  if curWorld != None:
    print(debug.clrcodes.fg.BLUE + "curWorld: " + curWorld.name + ", map:" + debug.clrcodes.fg.WHITE)
    curWorld.print()
    print(debug.clrcodes.fg.BLUE + "entity test:" + debug.clrcodes.fg.WHITE)
    debug.objprint(curWorld.getEntity(4, 2), True)







