from te2.ecs.entityMgr import EntityFactory
from te2.ecs.systemMgr import SystemFactory


entf = EntityFactory()
sysf = SystemFactory()

entf.componentLib.defineComponent(name = "visualComponent",
  values = {
    "name" : "Thicc Monke",
    "desc" : "A bigass mofo monke."
  }
)
entf.componentLib.defineComponent(name = "weightComponent", 
  values = {
    "weight" : 320
  }
)

def printInfo(entity): #create system function
  print("NAME:", entity.__components["visualComponent"]["name"])
  print("\tDESCRIPTION:", entity.__components["visualComponent"]["desc"])
  print("\tWEIGHT:", entity.__components["weightComponent"]["weight"])

sysf.newSystem(systemName="printInfo",componentsToProcess=["visualComponent","weightComponent"],function=printInfo) #define system for function

entities = []
entities.append(
  entf.newEntity(
    components=[
      entf.componentLib.newComponent("visualComponent"),
      entf.componentLib.newComponent("weightComponent"),
    ]
  )
)

sysf.runSystem("printInfo", entities)