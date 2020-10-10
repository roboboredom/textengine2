class ComponentLib:
  """
  A library of defined components.
  """
  def __init__(self):
    self.__components = {}
  
  def defineComponent(self, name: str, values: dict):
    """
    Define a new component for the library.
    Name: name of component.
    Values: dict of values to store in the component.
    """
    if name in self.__components: 
      raise Exception("Cannot define component \""+name+"\", name already taken.")
    else:
      self.__components[name] = values #add name : values to __components
  
  def newComponent(self, name: str) -> tuple:
    """
    Returns component as a tuple, for use by an entity.
    """
    if name in self.__components:
      return (name, self.__components[name]) #return (name, values)
    else:
      raise Exception("Component \""+name+"\" is not defined.")