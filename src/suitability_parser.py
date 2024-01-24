#!/usr/bin/env python3

import json
import string

def get_suitabilities() -> dict[list[dict]]:
    """Parses game dump json and gets pal suitabilities"""

    #Define Suitability Lists
    suitabilites: dict[list[dict]] = {
        'Watering': [],
        'Kindling':[],
        'Planting': [],
        'Generating Electricity': [],
        'Handiwork': [],
        'Gathering': [],
        'Lumbering': [],
        'Mining': [],
        'Medicine Production': [],
        'Cooling': [],
        'Transporting': [],
        'Farming': []
    }

    # Grab data from files
    with open('data/DT_PalMonsterParameter.json') as file:
        pal_parameters: dict[dict] = json.load(file)[0]['Rows']

    with open('data/DT_PalNameText.json') as file:
        pal_names: dict[dict] = json.load(file)[0]['Rows']

    # Iterate over all pals
    for pal, data in pal_parameters.items():
        
        # Skip bosses and gyms
        if "BOSS_" in pal or "GYM_" in pal:
            continue

        # Get pal name, skip if en_text
        try:
            name = pal_names["PAL_NAME_" +pal]['TextData']['LocalizedString']
            if name == "en_text":
                continue
        except KeyError:
            print(f"Could not find PAL '{pal}' in Pal Names.")
            continue

        food_level = data["FoodAmount"]
        pal_num = str(data["ZukanIndex"]) + data["ZukanIndexSuffix"]
        if pal_num == "-1":
            pal_num = "n/a"

        # Get suitability levels
        suitability_levels = {
            'Kindling' : data["WorkSuitability_EmitFlame"],
            'Watering' : data["WorkSuitability_Watering"],
            'Planting' : data["WorkSuitability_Seeding"],
            'Generating Electricity' : data["WorkSuitability_GenerateElectricity"],
            'Handiwork' : data["WorkSuitability_Handcraft"],
            'Gathering' : data["WorkSuitability_Collection"],
            'Lumbering' : data["WorkSuitability_Deforest"],
            'Mining' : data["WorkSuitability_Mining"],
            # 'oil_level' : data["WorkSuitability_OilExtraction"],
            'Medicine Production' : data["WorkSuitability_ProductMedicine"],
            'Cooling' : data["WorkSuitability_Cool"],
            'Transporting' : data["WorkSuitability_Transport"],
            'Farming' : data["WorkSuitability_MonsterFarm"]
        }

        for suitability, level in suitability_levels.items():
            if level > 0:
                pal_data = {
                    'name': name,
                    'pal_num': pal_num,
                    'level': level,
                    'food_level': food_level,
                }
                suitabilites[suitability].append(pal_data)
    return suitabilites

def create_wikitable(suitabilities: dict) -> list[str]:
    """Generates wikitable strings from suitability dict"""

    wikitables = []

    # iterate suitabilities
    for suitability, data in suitabilities.items():
        table = f"""{suitability}
{{| class="wikitable sortable mw-collapsible"
|+
!Pal
!No.
!{{{{i|{suitability}|notext}}}} Level
!Food
"""
        # Add every pal to table
        for pal in data:
            entry = f"""|-
|{{{{i|{pal['name']}}}}}
|{pal['pal_num']}
|{pal['level']}  
|{pal['food_level']}      
"""
            table += entry
        # Add closing string
        table += "|}\n"
        wikitables.append(table)

    return wikitables

        

def main():
    suitabilites_list = get_suitabilities()

    wiki_tables = create_wikitable(suitabilites_list)

    for table in wiki_tables:
        print(table)

if __name__ == "__main__":
    main()