class BaseEntity: 
  """
  Base class for an entity which holds data for a handler to read.
  """
  def __init__(self, name=None, symbol=None, x=0, y=0, shell=False): #called on instance creation
    if not shell:
      self.name = name
      self.symbol = symbol #symbol representing this object
      self.x = x
      self.y = y