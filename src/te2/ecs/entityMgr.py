from te2.ecs.componentMgr import ComponentLib

class EntityFactory():
  """
  Entity factory, used to create new unique entities from components.
  Has a component library it pulls from.
  """
  def __init__(self):
    self.__curID = 0
    self.componentLib = ComponentLib()
  
  def __newID(self):
    self.__curID += 1
    return self.__curID
  
  def newEntity(self, components=[]):
    """Returns a new entity with specified components & a unique ID."""
    return EntityFactory.__Entity(self.__newID(), components)

  class __Entity:
    """
    Entity, which has an ID and holds components.
    """
    def __init__(self, ID, components: list):
      self.ID = ID
    
      self.__components = {}
      for c in components:
        self.__components[c[0]] = c[1]
      
    def addComponent(self, component: tuple):
      """Add a component to this entity."""
      self.__components[component[0]] = component[1]
    
    def delComponent(self, name: str):
      """Remove a component from this entity."""
      del self.__components[name]




        

