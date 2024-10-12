local _, addonTable = ...

local function render_stats_priority(stats)
    local stat_names = {}
    for idx, stat in ipairs(stats) do
        local name_str;
        if (idx == 1) then
            name_str = "|cffff8001" .. stat["name"] .. "|r"
        elseif (idx == 2) then
            name_str = "|cffbc01f2" .. stat["name"] .. "|r"
        elseif (idx == 3) then
            name_str = "|cff2fff00" .. stat["name"] .. "|r"
        else            
            name_str = stat["name"]
        end

        table.insert(stat_names, name_str)
    end
    return table.concat(stat_names," > ")
end

SLASH_MURLOCKHELPER1 = "/mh"
SLASH_MURLOCKHELPER2 = "/murlockhelper"
SlashCmdList["MURLOCKHELPER"] = function(msg)
    local currentSpec = GetSpecialization()
    local className, _, playerClassId = UnitClass("player")
    local _, specName = GetSpecializationInfoForClassID(playerClassId, currentSpec)

    print("You are a", specName, className)

    local secondary_stats_list = render_stats_priority(addonTable.classes_stats[string.lower(className)][string.lower(specName)]["secondary_stats"])
    local minor_stats_list = render_stats_priority(addonTable.classes_stats[string.lower(className)][string.lower(specName)]["minor_stats"])
    print("Your recommended stats priority based on 2v2 statistics are:")
    print(secondary_stats_list)
    print(minor_stats_list)
end