#debug.py - debug, system, console stuff
import platform

class clrcodes: #ascii color escape codes
  class fg:
    BLACK   = "\u001b[30m"
    RED     = "\u001b[31m"
    GREEN   = "\u001b[32m"
    YELLOW  = "\u001b[33m"
    BLUE    = "\u001b[34m"
    MAGENTA = "\u001b[35m"
    CYAN    = "\u001b[36m"
    WHITE   = "\u001b[37m"
  class bg:
    BLACK     = "\033[40m"
    RED       = "\033[41m"
    GREEN     = "\033[42m"
    ORANGE    = "\033[43m"
    BLUE      = "\033[44m"
    PURPLE    = "\033[45m"
    CYAN      = "\033[46m"
    LIGHTGREY = "\033[47m"

def platformName(): #return os name (linux, windows)
  return platform.system()

def platformCheck(): #check if system compatible, log info
  s = platform.system()
  if s == "Linux": # linux
    print(clrcodes.fg.BLUE, "Running on Linux. [SUPPORTED]", clrcodes.fg.WHITE, sep = "")
  elif s == "Windows": # windows
    print(clrcodes.fg.BLUE, "Running on Windows. [SUPPORTED]", clrcodes.fg.WHITE, sep = "")
  else: # other os
    print(clrcodes.fg.RED, "\tRunning on unknown OS. [NOT SUPPORTED] Things may not work!", clrcodes.fg.WHITE, sep = "")

def objprint(obj, compact=False):
  """ 
  prints a json-style snippet containing all instance vars of an obj
  set compact=True for no newlines                                   
  """
  print(clrcodes.fg.GREEN, end="")
  
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
    
  print(clrcodes.fg.WHITE, end="")
