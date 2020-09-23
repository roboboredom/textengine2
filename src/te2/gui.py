import os
import tkinter 
#import turtle
from functools import partial
from tkinter import filedialog
from te2.logger import Logger

class GUI(tkinter.Tk):
  """
  GUI class, tkinter-based gui for controlling a game session.
  Only supports Windows OS.
  """
  def __init__(self, session):
    """session: game session to control"""
    tkinter.Tk.__init__(self) #call the __init__ of the class we inherited from first
    
    #non-tkinter instance vars
    self.session = session #game session to control
    self.__nextCommand = None #prefix private vars w/ "__"
    
    #tkinter instance vars
    self.wm_iconphoto(False, tkinter.PhotoImage(file=os.getcwd()+"\\game\\assets\\icon.png")) #set icon
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
    #self.mapPen = turtle.RawTurtle(canvas=self.mapCanvas) #assign turtle to canvas for rendering graphics
    #self.mapPen.speed(0) #disable turtle animation
    #self.mapPen.shape('square')
    #self.mapPen.hideturtle()
    #self.mapPen.screen.tracer(0, 0) #disable turtle screen refresh
    #self.mapPen.color("white") #set turtle color
    #self.mapPen.screen.bgcolor("black") #set turtle screen color

  #public functions
  def startLoop(self): #mainloop, function calls itself until told to stop
    Logger.log("Starting GUI loop.", color="red")
    self.focus_set() #give game window focus
    while True:
      if self.__nextCommand != "quit": #special interface only command, exits interface 
        if self.__nextCommand != None:
          self.session.runCommand(self.__nextCommand) #do stuff with command, then proceed
          self.__nextCommand = None #reset for next loop
        
          #self.__drawWorld()

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
  #def __drawWorld(self):
  #  pass

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
