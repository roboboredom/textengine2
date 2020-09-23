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

  @staticmethod
  def objPrint(obj, compact=False):
    """
    prints snippet containing instance data for an object
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
