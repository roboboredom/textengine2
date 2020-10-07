class ActQueue:
  """
  Class for a queue of acts, to be used by a world.
  """
  def __init__(self, world):
    self.world = world
    self.queue = []

  def addAct(self, act):
    """add act to quene"""
    self.queue.append(act)
  
  def clearActs(self):
    self.queue = []

  def doEntityLoop(self):
    """Preform one catch-act-queue loop on all entities in the world."""
    for entity in self.world.entities:
      for act in self.queue:
        for handler in entity.handlers:
          method = handler
          method(actor=entity, act=act, queue=self)
