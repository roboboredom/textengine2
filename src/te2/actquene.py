class ActQuene:
  """
  Class for a quene of acts, to be used by a world.
  """
  def __init__(self, world):
    self.world = world
    self.quene = []

  def addAct(self, act):
    """add act to quene"""
    self.quene.append(act)
  
  def clearActs(self):
    self.quene = []

  def cycle(self):
    pass
