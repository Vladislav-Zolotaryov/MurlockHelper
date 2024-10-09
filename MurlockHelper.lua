local _, addonTable = ...

local currentSpec = GetSpecialization()
local className, _, playerClassId = UnitClass("player")
local _, specName = GetSpecializationInfoForClassID(playerClassId, currentSpec)
print("Hello, you are a", specName, className)
print("Your recommended top stat is", addonTable.classes_stats[string.lower(className)][string.lower(specName)]["secondary_stats"][1]["name"])