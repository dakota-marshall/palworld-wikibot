#!/usr/bin/env python3
import json
import dataclasses
from dataclasses import asdict

@dataclasses.dataclass
class PartnerSkill:

  pal_name: str = ""
  skill_name: str = ""
  pal_num: str = ""
  skill_type: str = ""
  description: str = ""

@dataclasses.dataclass
class SkillList:
  skills: list[dict]

def get_partner_skills() -> list[dict]:
  # Load Necessary Files
  with open('data/DT_PalMonsterParameter.json') as file:
    pal_parameters: dict[dict] = json.load(file)[0]['Rows']

  with open('data/DT_PalNameText.json') as file:
    pal_names: dict[dict] = json.load(file)[0]['Rows']

  with open('data/DT_SkillNameText.json') as file:
    skill_names: dict[dict] = json.load(file)[0]['Rows']

  with open('data/DT_PalFirstActivatedInfoText.json') as file:
    skill_description: dict[dict] = json.load(file)[0]['Rows']

  # Create Skill list
  partner_skills = SkillList([])

  # Parse Data out of the files
  for pal, data in pal_parameters.items():

    skill_data = PartnerSkill()

    if "BOSS_" in pal or "GYM_" in pal:
        continue

    # Get pal name, skip if en_text
    try:
        skill_data.pal_name = pal_names["PAL_NAME_" +pal]['TextData']['LocalizedString']
        if skill_data.pal_name == "en_text":
            continue
    except KeyError:
        print(f"Could not find PAL '{pal}' in Pal Names.")
        continue
    
    skill_data.pal_num = str(data["ZukanIndex"]) + data["ZukanIndexSuffix"]
    if skill_data.pal_num == "-1":
        skill_data.pal_num = "n/a"

    # Get Partner Skill Name
    try:
      skill_data.skill_name = skill_names["PARTNERSKILL_"+pal]['TextData']['LocalizedString']
      if skill_data.skill_name.lower() == "en text":
        continue
    except KeyError:
       print(f"Could not find Skill for Pal '{pal}'.")
        
    # Get Skill Description
    try:
      skill_data.description = skill_description['PAL_FIRST_SPAWN_DESC_'+pal]['TextData']['LocalizedString']
    except KeyError:
       print(f"Could not find description for skill '{skill_data.skill_name}'")
    
    # Append to skill list
    partner_skills.skills.append(asdict(skill_data))
  
  return partner_skills.skills


def main():

  print(get_partner_skills())

if __name__ == "__main__":
  main()