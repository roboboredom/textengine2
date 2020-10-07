class Components:
  """
  Class w/ methods that return a formatted component for placement in an entity.
  Non-instantiable.
  """
  def __new__(cls, *args, **kw): # prevent instantiation
	  raise TypeError("Non-instantiable class!")
  
  @staticmethod
  def positionComponent(coords: tuple, canShareTile: bool) -> tuple: # the ":" type & "->" returntype hints are just used by the IDE, not python.
    return (
      "positionComponent", 
      {
        "coords" : coords,
        "canShareTile" : canShareTile
      }
    )
    
  @staticmethod
  def visualComponent(name: str, desc: str) -> tuple:
    return (
      "visualComponent", 
      {
        "name" : name,
        "desc" : desc
      }
    )

  @staticmethod
  def healthComponent(hp: int, maxhp: int) -> tuple:
    return (
      "healthComponent", 
      {
        "hp" : hp,
        "maxhp" : maxhp
      }
    )