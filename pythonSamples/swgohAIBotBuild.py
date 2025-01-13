# Script that retrieves player information in the mobile game SWGOH. I was planning to use OpenAI to analyse for player trends and give combat insights.
import openai
import requests
import pandas

endpoint = r"https://swgoh.gg/api/player/614868687/"
get_data = requests.get(url=endpoint).json()
get_characters = get_data["units"]
columns = []
characters = []
for c in get_characters:
    c = dict(c)
    for keys, values in c.items():
        values = dict(values)
        characters.append(values)
        for key, value in values.items():
            if key in columns:
                pass
            else:
                columns.append(key)
pd_data = pandas.DataFrame(data=characters, columns=columns)
pd_data = pd_data.drop(columns=["base_id", "url", "gear", "stats", "stat_diffs", "zeta_abilities", "omicron_abilities", "ability_data", "mod_set_ids", "combat_type"])
pd_data["relic_tier"] = pd_data["relic_tier"] - 2
pd_data["relic_tier"] = pd_data["relic_tier"].replace(-1, 0)
pd_data.to_csv(path_or_buf=r"C:\Users\jerom\Documents\swgoh_roster.csv", index=False)
print(pd_data)
