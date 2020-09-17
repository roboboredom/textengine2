import platform
import te2.world
import tkinter as tk
from tkinter import filedialog

# ============================ CLASS DEFINITION =================================

loadedWorlds = {}
selectedWorld = None #current selected world in loadedWorlds

def processCommand(cmd):
  if isinstance(cmd, str):
    cmd = [cmd]
  global loadedWorlds, selectedWorld
  
  if cmd[0] == "save":
    if len(cmd) > 1 and len(cmd) <= 2: #command only accepts 2 args
      te2.world.saveWorldFile(loadedWorlds[cmd[1]]) #save world to textengine2/game/worlds
      print(clrcodes.fg.green + "Saved world \"" + cmd[1] + "\" to worlds folder." + clrcodes.fg.white)
    else:
      print(clrcodes.fg.red + "Invalid amount of arguments." + clrcodes.fg.white)
      
  elif cmd[0] == "load":
    if len(cmd) > 1 and len(cmd) <= 2: #command only accepts two arguments   
      world = te2.world.loadWorldFile(cmd[1]) #load world from textengine2/game/worlds/ 
      loadedWorlds[world.name] = world #add world to loadedWorlds
      del world
      print(clrcodes.fg.green + "Loaded world \"" + cmd[1] + "\" from worlds folder." + clrcodes.fg.white)
    else:
      print(clrcodes.fg.red + "Invalid amount of arguments." + clrcodes.fg.white)
  
  elif cmd[0] == "del":
    if len(cmd) > 1 and len(cmd) <= 2: #command only accepts two arguments 
      te2.world.delWorldFile(cmd[1]) #delete world from textengine2/game/worlds/
      print(clrcodes.fg.green + "Deleted world \"" + cmd[1] + "\" from worlds folder." + clrcodes.fg.white)
    else:
      print(clrcodes.fg.red + "Invalid amount of arguments." + clrcodes.fg.white)
  
  elif cmd[0] == "gen":
    if len(cmd) > 1 and len(cmd) <= 2:
      world = te2.world.World(cmd[1]) #generate new world
      loadedWorlds[world.name] = world #add world to loadedWorlds
      del world
    else:
      print(clrcodes.fg.red + "Invalid amount of arguments." + clrcodes.fg.white)
  
  elif cmd[0] == "sel":
    if len(cmd) > 1 and len(cmd) <= 2:
      selectedWorld = cmd[1] #set current world
    else:
      print(clrcodes.fg.red + "Invalid amount of arguments." + clrcodes.fg.white)
  
  elif cmd[0] == "help":
    if len(cmd) == 1:
      print(clrcodes.fg.green,
            "help\n",
            "\tshows this text\n",
            "save <worldname>\n",
            "\tsave world in loadedWorlds to folder \"worlds\"\n",
            "load <worldname>\n",
            "\tload world from folder \"worlds\" to loadedWorlds\n",
            "del  <worldname>\n",
            "\tdelete world from folder \"worlds\"\n",
            "gen  <worldname>\n",
            "\tgenerate new world, add it to loadedWorlds\n",
            "sel  <worldname>\n",
            "\tset selected world (in loadedWorlds)\n",
            clrcodes.fg.white, sep="")
    else:
      print(clrcodes.fg.red + "Invalid amount of arguments." + clrcodes.fg.white)

  elif cmd[0] == "lober": #flash that sexy thicc lober for the user
    if len(cmd) == 1:
      print("{1}d{0}u{1}m{0}m{1}y t{0}h{1}i{0}c{1}c{0} {1}r{0}e{1}d{0} {1}l{0}o{1}b{0}e{1}r{0}".format(clrcodes.fg.white, clrcodes.fg.red))

  else:
    print(clrcodes.fg.red + "[Error] No command \"" + cmd[0] + "\"" + clrcodes.fg.white)
  
  print(clrcodes.fg.green,end="")
  if selectedWorld != None:
    print(clrcodes.fg.green,end="")
    print("\nloadedWorlds:")
    print(loadedWorlds.keys())
    print("\nselectedWorld: " + loadedWorlds[selectedWorld].name + ", map: ")
    loadedWorlds[selectedWorld].print()
    print(clrcodes.fg.white)

class GUI(tk.Tk):  
  def __init__(self):
    tk.Tk.__init__(self) #call the __init__ of the class we inherited from first

    #tkinter instance vars
    self.wm_iconphoto(False, tk.PhotoImage(file="D:\\GitHub\\python\\textengine2\\game\\assets\\icon.png")) #set icon
    self.wm_title("Textengine2")
    self.resizable(False, False) #block resizing
    self.lift() #move window above all others
    
    #Main menu for window
    self.mainMenu = tk.Menu(master=self)
    self.config(menu=self.mainMenu)

    #Main menu - File dropdown menu
    self.fileMenu = tk.Menu(self.mainMenu, tearoff=0)
    
    self.fileMenu.add_command(label="Help", command=self.__helpCmd)
    self.fileMenu.add_command(label="Open world", command=self.__loadWorldCommand)
    self.fileMenu.add_separator()
    self.fileMenu.add_command(label="Quit", command=self.__quitCmd)
    self.fileMenu.add_separator()
    self.fileMenu.add_command(label="Lober", command=self.__loberCmd)

    self.mainMenu.add_cascade(label="File", menu=self.fileMenu)
    
    #Frame container for canvas
    self.mapFrame = tk.Frame(
      master=self,
      width=640, 
      height=480,
      borderwidth=10,
      relief="ridge",
      background="blue"
      )
    self.mapFrame.pack()

    #Canvas for drawing map
    self.mapCanvas = tk.Canvas(
      master=self.mapFrame,
      background="black"
      )
    self.mapCanvas.pack()

    #non-tkinter instance vars
    self.__nextCommand = None #prefix private vars w/ "__"
  
  #public functions
  def start(self):
    print(clrcodes.fg.red + "Starting GUI loop." + clrcodes.fg.white)
    self.focus_set() #give game window focus
    self.__doLoop() #start gui loop, continue below when exited
    
    print("passed self.__doLoop() in GUI.start()")
    #print(clrcodes.fg.red + "GUI closed by command \"quit\". Starting console loop." + clrcodes.fg.white)
    #self.destroy() #kill this GUI object
  
  #private functions
  def __doLoop(self): #mainloop, function calls itself until told to stop
    while True:
      if self.__nextCommand != "quit": #special interface only command, exits interface
        if self.__nextCommand != None:
          processCommand(self.__nextCommand) #do stuff with command, then proceed
          self.__nextCommand = None #reset for next loop
        
        try: #do tkinter processes
          self.update()
        except: #if the gui closed with close button
          print(clrcodes.fg.red + "GUI closed. Starting console loop." + clrcodes.fg.white)
          break
      
      else:
        print(clrcodes.fg.red + "GUI closed by File > Quit. Starting console loop." + clrcodes.fg.white)
        break
  
  def __helpCmd(self): self.__nextCommand = "help"
  def __quitCmd(self): self.__nextCommand = "quit"
  def __loberCmd(self): self.__nextCommand = "lober"
  
  def __loadWorldCommand(self):
    """open popup and ask user for file, then issue load command for file"""
    fileName = filedialog.askopenfilename(
      initialdir = "D:\\GitHub\\python\\textengine2\\game\\worlds\\",
      title = "Select a world file to open.",
      filetypes = (("textengine2 world file","*.te2wrld"),("all files","*.*"))
      )
    self.__setCommand("dirload " + fileName)

class clrcodes:
  """ascii color escape codes"""
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

def objPrint(obj, compact=False):
  """
  prints a json-style snippet containing all instance vars of an obj
  set compact=True for no newlines                                   
  """
  print(clrcodes.fg.blue, end="")

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

gui = GUI() #initalize game gui
gui.start() #start gui loop, stop on this line until gui killed

#console loop, alternative to gui loop
print(clrcodes.fg.green + ">>>> textengine2, by dawson gray <<<< \nType \"help\" for a list of commands." + clrcodes.fg.white)
while True:
  cmd = input("> ")
  if cmd != "" and cmd.isspace() == False: #check if cmd not just whitespace or empty
    processCommand(cmd.split())
  else: 
    print(clrcodes.fg.red + "Nothing entered." + clrcodes.fg.white)