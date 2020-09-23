import platform, os, time
from functools import partial
import te2.world #world class
import tkinter #tkinter gui library
from tkinter import filedialog
import turtle #turtle graphics

# ============================ CLASSES =========================================
class GUI(tkinter.Tk):
  """
  GUI class, tkinter-based gui for controlling a game session.
  """
  def __init__(self, session):
    """session: game session to control"""
    tkinter.Tk.__init__(self) #call the __init__ of the class we inherited from first
    
    #non-tkinter instance vars
    self.session = session #game session to control
    self.__nextCommand = None #prefix private vars w/ "__"
    
    #tkinter instance vars
    self.wm_iconphoto(False, tkinter.PhotoImage(file=os.getcwd()+"/game/assets/icon.png")) #set icon
    self.wm_title("textengine2")
    self.resizable(False, False)
    self.lift() #move window above all others

    #mainmenu
    self.mainMenu = tkinter.Menu(master=self)
    self.config(menu=self.mainMenu) #set default menu to mainMenu
    
    #mainmenu - file submenu - open world, quit
    self.fileMenu = tkinter.Menu(
      self.mainMenu, 
      tearoff=0,
      background="#000000",
      foreground="#C89D32",
      activebackground="#C89D32", 
      activeforeground="#000000"
      )
    self.fileMenu.add_command(label="Open world", command=self.__openWorldCommand)
    self.fileMenu.add_separator()
    self.fileMenu.add_command(label="Quit", command=partial(self.__setCommand, "quit"))
    self.mainMenu.add_cascade(label="File", menu=self.fileMenu)
    
    #mainmenu - help
    self.mainMenu.add_command(label="Help", command=partial(self.__setCommand, "help"))

    #frame container for canvas
    self.mapFrame = tkinter.Frame(
      master=self,
      width=640, 
      height=480,
      borderwidth=10,
      relief="ridge",
      background="#A57504"
      )
    self.mapFrame.pack()

    #canvas for turtle
    self.mapCanvas = tkinter.Canvas(
      master=self.mapFrame,
      background="black"
      )
    self.mapCanvas.pack()

    #turtle for drawing to canvas
    self.mapPen = turtle.RawTurtle(canvas=self.mapCanvas) #assign turtle to canvas for rendering graphics
    self.mapPen.speed(0) #disable turtle animation
    self.mapPen.shape('square')
    self.mapPen.hideturtle()
    self.mapPen.screen.tracer(0, 0) #disable turtle screen refresh
    self.mapPen.color("white") #set turtle color
    self.mapPen.screen.bgcolor("black") #set turtle screen color

  #public functions
  def startLoop(self): #mainloop, function calls itself until told to stop
    Logger.log("Starting GUI loop.", color="red")
    self.focus_set() #give game window focus
    while True:
      if self.__nextCommand != "quit": #special interface only command, exits interface
        if self.__nextCommand != None:
          self.session.runCommand(self.__nextCommand) #do stuff with command, then proceed
          self.__nextCommand = None #reset for next loop
          
          self.__drawWorld()
        
        try: #do tkinter processes
          self.update()
        except: #if the gui closed with close button
          Logger.log("GUI closed. Starting console loop.", color="red")
          break
      
      else:
        Logger.log("GUI closed by File > Quit. Starting console loop.", color="red")
        self.destroy()
        break
  
  #private functions
  def __drawWorld(self):
    pass

  def __setCommand(self, command): 
    self.__nextCommand = command
  
  def __openWorldCommand(self): #open popup and ask user for file, then issue load command for file
    path = filedialog.askopenfilename(
      initialdir = "D:\\GitHub\\python\\textengine2\\game\\worlds\\",
      title = "Select a world file to open.",
      filetypes = (("textengine2 worldfile","*.te2wrld"), ("all files","*.*"))
      )
    #arg to load should just be filename, no path or extensions!
    path = os.path.normpath(path) #normalize path
    path = path.split(os.sep) #split it into pieces, ex: "\\folder1\\folder2\\asd.txt" -> ['folder1', 'folder2', 'asd.txt']
    filename = path[len(path) - 1].split(".")[0] #get just filename
    self.__setCommand("load " + filename)

class Logger:
  """Logger class, better console output. Do not use as instance!"""
  
  colorcodes = { #ansi color codes
    "black"   : "\u001b[1m\u001b[30m",
    "red"     : "\u001b[1m\u001b[31m",
    "green"   : "\u001b[1m\u001b[32m",
    "yellow"  : "\u001b[1m\u001b[33m",
    "blue"    : "\u001b[1m\u001b[34m",
    "magenta" : "\u001b[1m\u001b[35m",
    "cyan"    : "\u001b[1m\u001b[36m",
    "white"   : "\u001b[1m\u001b[37m"
  }

  @staticmethod
  def log(*args, color="white", sep="", end="\n"):
    """
    log any number of objects to console
    
    *args: object(s) to log
    color= color of text, defaults to "white"
    sep= string to insert between objects, defaults to ""
    end= string to insert at end, defaults to "\\n"
    """
    print(Logger.colorcodes[color], end="")
    
    for i in range(0, len(args)):
      if i == len(args) - 1:
        print(args[i], end=end)
      else:
        print(args[i], end=sep)

    print(Logger.colorcodes["white"], end="")
  
class BaseEntity: 
  """base class for any entity in the world"""
  def __init__(self, name=None, symbol=None, x=0, y=0, shell=False): #called on instance creation
    if not shell:
      self.name = name
      self.symbol = symbol #symbol representing this object
      self.x = x
      self.y = y

class Session:
  """
  Session class, contains data for a game session,
  and has methods for manipulating that data.
  """
  def __init__(self):
    self.loadedWorlds = {}
    self.selectedWorld = None #current selected world in loadedWorlds
  
  def runCommand(self, cmd):
    """run a session command"""
    cmd = cmd.split(" ") #split cmd into pieces by spaces
    
    if cmd[0] == "save":
      if len(cmd) > 1 and len(cmd) <= 2: #command only accepts 2 args
        te2.world.World.saveWorldFile(self.loadedWorlds[cmd[1]]) #save world to textengine2/game/worlds
        Logger.log("Saved world \"", cmd[1], "\" to worlds folder.", color="green")
      else:
        Logger.log("Invalid amount of arguments.", color="red")
        
    elif cmd[0] == "load":
      if len(cmd) > 1 and len(cmd) <= 2: #command only accepts two arguments   
        world = te2.world.World.loadWorldFile(cmd[1]) #load world from textengine2/game/worlds/ 
        self.loadedWorlds[world.name] = world #add world to loadedWorlds
        del world
        Logger.log("Loaded world \"", cmd[1], "\" from worlds folder.", color="green")
      else:
        Logger.log("Invalid amount of arguments.", color="red")
    
    elif cmd[0] == "del":
      if len(cmd) > 1 and len(cmd) <= 2: #command only accepts two arguments 
        te2.world.World.delWorldFile(cmd[1]) #delete world from textengine2/game/worlds/
        Logger.log("Deleted world \"", cmd[1], "\" from worlds folder.", color="green")
      else:
        Logger.log("Invalid amount of arguments.", color="red")
    
    elif cmd[0] == "gen":
      if len(cmd) > 1 and len(cmd) <= 2:
        world = te2.world.World(cmd[1]) #generate new world
        self.loadedWorlds[world.name] = world #add world to loadedWorlds
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
          "del  <worldname>\n",
          "\tdelete world from folder \"worlds\"\n",
          "gen  <worldname>\n",
          "\tgenerate new world, add it to loadedWorlds\n",
          "sel  <worldname>\n",
          "\tset selected world (in loadedWorlds)\n",
          color="green", sep=""
        )
      else:
        Logger.log("Invalid amount of arguments.", color="red")
    
    else:
      Logger.log("No command \"", cmd[0], "\".", color="red")
    
    if self.selectedWorld != None:
      Logger.log("\nselectedWorld: ", self.loadedWorlds[selectedWorld].name)
      self.loadedWorlds[selectedWorld].print()

# ============================ FUNCTIONS =======================================
def platformCheck(): 
  """check if system compatible, log info"""
  s = platform.system()
  if s == "Linux": # linux
    Logger.log("Running on Linux. [SUPPORTED]", color="green")
  elif s == "Windows": # windows
    Logger.log("Running on Windows. [SUPPORTED]", color="green")
  else: # other os
    Logger.log("Running on unknown OS. [NOT SUPPORTED] Things may not work!", color="red")

def objPrint(obj, compact=False):
  """
  prints a json-style snippet containing all instance vars of an obj
  set compact=True for no newlines                                   
  """
  print(Logger.colorcodes["magenta"], end="")

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
    
  print(Logger.colorcodes["white"], end="")

# ============================ MAIN ============================================
session1 = Session() #new game session

gui = GUI(session1) #initalize game gui, assign it a session to control

gui.startLoop() #start gui loop, continue past here when it exits

Logger.log("Session ended!", color="red")