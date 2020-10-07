from te2.actqueue import ActQueue
from te2.acts import Acts
from te2.entity import Entity

class Handlers:
  """
  Handler methods called by listeners.
  """
  def damageHandler(actor: Entity, act: dict, queue: ActQueue):
    """Catches: damageAct"""
    if act["actName"] != "damageAct": #exit method if act not damageAct
      return
    if actor.components["positionComponent"]["coords"] == act["doneToCoords"]:
      actor.components["healthComponent"]["hp"] -= act["dmg"]
      queue.addAct(
        Acts.yellAct(
          actor.id,
          phrase = "Ouch! I only have " + str(actor.components["healthComponent"]["hp"]) + " hp now."
        )
      )