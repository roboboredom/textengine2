from te2.components import Components
from te2.handlers import Handlers

class Entity: 
  """
  Base class for an entity which holds components and handlers which modify the components.
  """
  def __init__(self, shell=False, components=[], handlers=[]):
    if not shell:
      self.id = None

      self.data = {
        "components" : {},
        "handlers" : {},
      }

      for component in components: 
        self.data["components"][component[0]] = component[1]
      for handler in handlers:
        self.data["handlers"][handler[0]] = handler[1]



        

