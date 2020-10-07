from te2.components import Components

class Entity: 
  """
  Base class for an entity which holds components & listeners.
  Components are variable storage for an entity.
  Listeners are groups of acts to listen for, and what handler method to call when heard.
  """
  def __init__(self, shell=False, components=[], handlers=[]):
    if not shell:
      self.id = None
      
      self.components = {}
      for component in components: 
        self.components[component[0]] = component[1]
      
      self.handlers = handlers



        

