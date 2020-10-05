class Acts:
  """
  Class w/ methods that return a formatted act for placement in a quene.
  Non-instantiable.
  """
  def __new__(cls, *args, **kw): # prevent instantiation
	  raise TypeError("Non-instantiable class!")

  @staticmethod
  def damageAct(actorId: int, doneTo: tuple, dmg: int):
    return {
      "actName": "damageAct",

      "actorId": actorId,
      "doneTo": doneTo,
      "dmg": dmg
    }
  
  @staticmethod
  def yellAct(actorId: int, phrase: str):
    return {
      "actName": "yellAct",

      "actorId": actorId,
      "phrase": phrase
    }

  @staticmethod
  def moveAct(actorId: int, movedTo: tuple):
    return {
    "actName": "moveAct",

    "actorId": actorId,
    "movedTo": movedTo
    }