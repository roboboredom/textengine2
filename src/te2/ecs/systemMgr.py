def isKeyInDict(k: str, d: dict) -> bool:
  if k in d: 
    return True
  else: 
    return False

class SystemFactory:
  """
  System manager, used to define and run systems.
  Systems are passed a function which gets called with any
  entity (that contained a component the system is defined
  to process) as an argument.
  """
  def __init__(self):
    self.__systems = {}

  def newSystem(self, systemName, componentsToProcess, function):
    self.__systems[systemName] = SystemFactory.__System(componentsToProcess, function)

  def runSystem(self, systemName, entityList):
    for ent in entityList:
      for comp in self.__systems[systemName].componentsToProcess:
        
        print(comp)
        if isKeyInDict(comp, ent.__components) == True:
          self.__systems[systemName].process(ent)
  
  class __System:
    """
    A system.
    """
    def __init__(self, componentsToProcess, function):
      self.componentsToProcess = componentsToProcess
      self.function = function
    
    def process(self, entity):
      self.function(entity)


