import requests
from bs4 import BeautifulSoup

class_data = {
    "death-knight": [
        "blood", "frost", "unholy"
    ],
    "demon-hunter": [
        "havoc", "vengeance"
    ],
    "druid": [
 	    "balance", "feral", "guardian", "restoration"
    ],
    "evoker": [
        "devastation", "preservation", "augmentation"
    ],
    "hunter": [
        "beast-mastery", "marksmanship", "survival"
    ],
    "mage": [
        "arcane", "fire", "frost"
    ],
    "monk": [
        "brewmaster", "mistweaver", "windwalker"
    ],
    "paladin": [
        "holy", "protection", "retribution"
    ],
    "priest": [
        "discipline", "holy", "shadow"
    ],
    "rogue": [
     	"assassination", "outlaw", "subtlety"
    ],
    "shaman": [
        "elemental", "enhancement", "restoration"
    ],
    "warlock": [
 	    "affliction","demonology", "destruction"
    ],
    "warrior": [
        "arms", "fury", "protection"
    ],
}

game_mode_name = "2v2"

def parse_stat_priority(stat_priorities, stats_count, divs_per_stat):
    stat_divs_count = stats_count * divs_per_stat
    actual_stats_div_count = len(stat_priorities) 
    if actual_stats_div_count != stat_divs_count:
        print("Unexpected count of divs in stats block:", actual_stats_div_count)
        return []

    results = []
    n = 0
    for stat_idx in range(0, stats_count):
        start = n
        end = n + divs_per_stat
        n = end

        stat_slice = stat_priorities[start:end]
        
        heigh_div = stat_slice[0].get_text()
        value_div = int(stat_slice[1].get_text().replace("+", ""))
        percentage_div, name_div = stat_slice[2].get_text().split(" ", maxsplit=1)

        results.append({ "value": value_div, "name": name_div, "percentage": percentage_div})

    results.sort(key = lambda stat: stat["value"], reverse=True)
    return results


def data_url(class_name, spec_name, game_mode_name):
    return f"https://murlok.io/{class_name}/{spec_name}/{game_mode_name}"


class_stats_from_api = {}
for class_name, spec_names in class_data.items():
    spec_stats_dict = {}
    for spec_name in spec_names:
        url = data_url(class_name, spec_name, game_mode_name)

        try:
            html = requests.get(url).text
            soup = BeautifulSoup(html, features="lxml")

            secondary_stat_priority_divs = soup.select(".guide-stats-size-4 .guide-stats-chart-item > div")
            minor_stat_priority_divs = soup.select(".guide-stats-size-3 .guide-stats-chart-item > div")

            secondary_stats = parse_stat_priority(secondary_stat_priority_divs, stats_count = 4, divs_per_stat = 3)
            minor_stats = parse_stat_priority(minor_stat_priority_divs, stats_count = 3, divs_per_stat = 3)

            spec_stats_dict[spec_name] = {
                "secondary_stats": secondary_stats,
                "minor_stats": minor_stats,
            }
        except Exception as e:
            print("Failed to retrieve data for", class_name, spec_name, repr(e))
    class_stats_from_api[class_name] = spec_stats_dict


import json
with open('stats.json', 'w') as fp:
    json.dump(class_stats_from_api, fp)
