from entityfactory import EntityFactory


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
    for entity in entityList:
      for component in self.__systems[systemName].componentsToProcess:
        if component in entity.__components:
          self.__systems[systemName].process(entity)
  
  class __System:
    """
    A system.
    """
    def __init__(self, componentsToProcess, function):
      self.componentsToProcess = componentsToProcess
      self.function = function
    
    def process(self, entity):
      self.function(entity)


if __name__ == "__main__":
  entf = EntityFactory()
  sysf = SystemFactory()

  entf.componentLib.defineComponent(name = "visualComponent",
    values = {
      "name" : "Thicc Monke",
      "desc" : "A bigass mofo monke."
    }
  )
  entf.componentLib.defineComponent(name = "weightComponent", 
    values = {
      "weight" : 320
    }
  )
  
  def printInfo(entity):
    print("NAME:", entity.__["visualComponent"]["name"])
    print("\tDESCRIPTION:", entity.__["visualComponent"]["desc"])
    print("\tWEIGHT:", entity.__["weightComponent"]["weight"])

  sysf.newSystem(
    systemName = "printInfo",
    componentsToProcess = [
      "visualComponent"
      "weightComponent"
    ],
    function = printInfo
  )

  entlist = []
  entlist.append(entf.newEntity(components=[
    entf.componentLib.newComponent("visualComponent"),
    entf.componentLib.newComponent("weightComponent"),
  ]))

  sysf.runSystem("printInfo", entlist)
