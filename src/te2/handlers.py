class Handlers:
  """
  Class w/ formatted handlers for placement in an entity.
  Also contains the actual handler methods.
  Non-instantiable.
  """
  damageHandler = (
    "damageHandler", {
      "triggers" : [
        "damageAct",
      ]
    }
  )

  def __new__(cls, *args, **kw): # prevent instantiation
	  raise TypeError("Non-instantiable class!")
