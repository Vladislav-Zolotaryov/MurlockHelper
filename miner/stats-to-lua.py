import json
from textwrap import dedent

class_stats_from_api = {}

with open('stats.json', 'r') as fp:
    class_stats_from_api = json.load(fp)


def format_stats_block_lua(stats_block):
    results = []
    for i, x in enumerate(stats_block):
        results.append(
                    """
                    [{idx}] = {{
                        value = {value},
                        name = "{name}",
                        percentage = "{percentage}"
                    }}""".format(idx=i+1, value=x["value"], name=x["name"], percentage=x["percentage"])
                )
    return ",".join(results)
 
lua_root = "stats = {}"


classes_lua = []
for class_name, specs in class_stats_from_api.items():
    specs_lua = []
    for spec, stats in specs.items():
        secondary_stats_block_lua = format_stats_block_lua(stats["secondary_stats"])
        minor_stats_block_lua = format_stats_block_lua(stats["minor_stats"])
        if stats["secondary_stats"] and stats["minor_stats"]:
            spec_lua = """\
        {spec} = {{
                secondary_stats = {{\
                    {secondary_stats_block_lua},
                }},
                minor_stats = {{\
                    {minor_stats_block_lua}
                }}
        }}""".format(spec=spec.replace("-", "_"), secondary_stats_block_lua=secondary_stats_block_lua, minor_stats_block_lua=minor_stats_block_lua)
            specs_lua.append(spec_lua)

    class_lua = """\
    {class_name} = {{
    {specs_lua}
    }}""".format(class_name=class_name.replace("-", "_"), specs_lua=",\n".join(specs_lua))
    classes_lua.append(class_lua)

final_lue = "local addonName, addonTable = ...;\naddonTable.classes_stats = {\n" + ",\n".join(classes_lua) + "\n}"

with open('Stats.lua', 'w') as fp:
    fp.write(final_lue)