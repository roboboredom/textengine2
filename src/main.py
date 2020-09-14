import platform
import te2.world #world class, functions

# ============================ CLASS DEFINITION =================================
class clrcodes: #ascii color escape codes
  class fg:
    black   = "\u001b[30m"
    red     = "\u001b[31m"
    green   = "\u001b[32m"
    yellow  = "\u001b[33m"
    blue    = "\u001b[34m"
    magenta = "\u001b[35m"
    cyan    = "\u001b[36m"
    white   = "\u001b[37m"
  class bg:
    black   = "\033[40m"
    red     = "\033[41m"
    green   = "\033[42m"
    orange  = "\033[43m"
    blue    = "\033[44m"
    purple  = "\033[45m"
    cyan    = "\033[46m"
    grey    = "\033[47m"

class BaseEntity: #base class for any entity in the world 
  def __init__(self, name=None, symbol=None, x=0, y=0, shell=False): #called on instance creation
    if not shell:
      self.name = name
      self.symbol = symbol #symbol representing this object
      self.x = x
      self.y = y

# ============================ FUNCTION DEFINITIONS ============================
def platformCheck(): 
  #check if system compatible, log info
  s = platform.system()
  if s == "Linux": # linux
    print(clrcodes.fg.blue, "Running on Linux. [SUPPORTED]", clrcodes.fg.white, sep = "")
  elif s == "Windows": # windows
    print(clrcodes.fg.blue, "Running on Windows. [SUPPORTED]", clrcodes.fg.white, sep = "")
  else: # other os
    print(clrcodes.fg.red, "\tRunning on unknown OS. [NOT SUPPORTED] Things may not work!", clrcodes.fg.white, sep = "")

def objprint(obj, compact=False):
  #prints a json-style snippet containing all instance vars of an obj
  #set compact=True for no newlines                                   
  print(clrcodes.fg.green, end="")
  
  if compact:
    print(obj.__class__.__name__," 0x",id(obj)," {",sep="",end="")
    index = 0 #use this to tell when we are on the last key so we don"t put that last comma
    for key in obj.__dict__.keys():
      if key != "__dict__":
        if index == len(obj.__dict__.keys()) - 1: #-1 to not count the __dict__ key thing
          print("\"",key,"\":\"",obj.__dict__[key],"\"}\n",sep="")
        else:
          print("\"",key,"\":\"",obj.__dict__[key],"\",",sep="",end="")
      index += 1
  else:
    print(obj.__class__.__name__," 0x",id(obj),"\n{",sep="")
    index = 0 #use this to tell when we are on the last key so we don"t put that last comma
    for key in obj.__dict__.keys():
      if key != "__dict__":
        if index == len(obj.__dict__.keys()) - 1: #-1 to not count the __dict__ key thing
          print("\"",key,"\":\"",obj.__dict__[key],"\"\n}\n",sep="")
        else:
          print("\"",key,"\":\"",obj.__dict__[key],"\",",sep="")
      index += 1
    
  print(clrcodes.fg.white, end="")

# ============================ MAIN ============================================
platformCheck()
print(clrcodes.fg.green, ">>>>>> textengine2 || by dawson gray <<<<<< \nType \"help\" for a list of commands.\n", clrcodes.fg.white, sep="")

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
          curWorld = te2.world.World(cmd[1])
          
          curWorld.insertCopyAt(t_rock, 2, 3) #EXAMPLE FILLER ENTITIES
          curWorld.insertCopyAt(t_rock, 1, 1) 
          curWorld.insertCopyAt(t_bush, 4, 2)
          
          te2.world.saveWorldFile(curWorld) #save world to textengine2/src/worlds
          
          print(clrcodes.fg.green + "Saved world \"" + cmd[1] + "\" to worlds folder." + clrcodes.fg.white)
        except:
          print(clrcodes.fg.red + "World name \"" + cmd[1] + "\" cannot be used as filename." + clrcodes.fg.white)
      else:
        print(clrcodes.fg.red + "Invalid amount of arguments." + clrcodes.fg.white)
        
    elif cmd[0] == "load":
      if len(cmd) > 1 and len(cmd) <= 2: #command only accepts two arguments 
        try:
          curWorld = te2.world.loadWorldFile(cmd[1]) #load world from textengine2/src/worlds/ 
          
          print(clrcodes.fg.green + "Loaded world \"" + cmd[1] + "\" from worlds folder." + clrcodes.fg.white)
        except:
          print(clrcodes.fg.red + "No world named \"" + cmd[1] + "\" saved." + clrcodes.fg.white)
      else:
        print(clrcodes.fg.red + "Invalid amount of arguments." + clrcodes.fg.white)
    
    elif cmd[0] == "del":
      if len(cmd) > 1 and len(cmd) <= 2: #command only accepts two arguments 
        try:
          te2.world.delWorldFile(cmd[1]) #load world from textengine2/src/worlds/
          
          print(clrcodes.fg.green + "Deleted world \"" + cmd[1] + "\" from worlds folder." + clrcodes.fg.white)
        except:
          print(clrcodes.fg.red + "No world named \"" + cmd[1] + "\" saved." + clrcodes.fg.white)
      else:
        print(clrcodes.fg.red + "Invalid amount of arguments." + clrcodes.fg.white)
    
    elif cmd[0] == "help":
      if len(cmd) == 1:
        print(clrcodes.fg.green +
              "save <worldname>\n" +
              "load <worldname>\n" +
              "del <worldname>\n" +
              "help" + clrcodes.fg.white)
      else:
        print(clrcodes.fg.red + "Invalid amount of arguments." + clrcodes.fg.white)

    else:
      print(clrcodes.fg.red + "Invalid command." + clrcodes.fg.white)
  else: 
    print(clrcodes.fg.red + "No command entered." + clrcodes.fg.white)
    
  if curWorld != None:
    print(clrcodes.fg.blue + "curWorld: " + curWorld.name + ", map:")
    curWorld.print()
    print("entity test:" + clrcodes.fg.white)
    objprint(curWorld.getEntity(4, 2), True)







