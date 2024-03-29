#!/usr/bin/env python3
import json
import dataclasses
from dataclasses import asdict

@dataclasses.dataclass
class Item:
  recipe: dict
  name: str = ""
  item_type: str = ""
  description: str = ""
  weight: float = 0
  rarity: str = ""
  buy_price: int = 0
  sell_price: int = 0
  durability: int = 0
  mag_size: int = 0
  attack: int = 0
  armor_hp: int = 0
  armor_def: int = 0
  shield_value: int = 0
  consumable: bool = False

def get_items() -> list[dict]:

  with open('data/DT_ItemDataTable.json') as file:
    item_data: dict[dict] = json.load(file)[0]['Rows']

  with open('data/DT_ItemDescriptionText.json') as file:
    item_descriptions: dict[dict] = json.load(file)[0]['Rows']

  with open('data/DT_ItemNameText.json') as file:
    item_names: dict[dict] = json.load(file)[0]['Rows']

  with open('data/DT_ItemRecipeDataTable.json') as file:
    item_recipes: dict[dict] = json.load(file)[0]['Rows']

  item_list = []

  for item_name, data in item_data.items():

    item = Item({})

    item.item_type = data['TypeA'].replace('EPalItemTypeA::', '')
    item.weight = data['Weight']
    item.buy_price =  data['Price']
    if item.buy_price == 1:
      item.sell_price = 1
    else:
      item.sell_price = (item.buy_price / 10)
    #item.consumable = not data['bNotConsumed']
    if item.item_type == "Food" or item.item_type == "Consume":
      item.consumable = not data['bNotConsumed']
    else:
      item.consumable = False
    item.durability = data['Durability']
    item.mag_size = data['MagazineSize']
    item.attack = data['PhysicalAttackValue']
    item.armor_hp = data['HPValue']
    item.armor_def = data['PhysicalDefenseValue']
    item.shield_value = data['ShieldValue']

    # Item Name
    try:
      item.name = item_names["ITEM_NAME_"+item_name]['TextData']['LocalizedString']
      # try and grab the root name for upgraded variants if en_text
      if item.name == "en Text":
          item.name = item_names["ITEM_NAME_"+item_name[:-2]]['TextData']['LocalizedString']
    except KeyError:
      print(f"Failed to find name for {item_name}")
      continue

    # Item Description
    try:
      item.description = item_descriptions["ITEM_DESC_"+item_name]['TextData']['LocalizedString']
      if item.description == "en Text":
        item.description = item_descriptions["ITEM_DESC_"+item_name[:-2]]['TextData']['LocalizedString']
    except KeyError:
      print(f"Failed to get description for {item_name}")
      continue

    # Rarity
    match data['Rarity']:
      case 0:
        item.rarity = "Common"
      case 1:
        item.rarity = "Uncommon"
      case 2:
        item.rarity = "Rare"
      case 3:
        item.rarity = "Epic"
      case 4:
        item.rarity = "Legendary"

    # Get Recipe
    try:
      for field, data in item_recipes[item_name].items():
        match field:
          case "Material1_Id":
            if data != "None":
              item.recipe['mat1_id'] = item_names["ITEM_NAME_"+data]['TextData']['LocalizedString']
          case "Material1_Count":
            if data != 0:
              item.recipe['mat1_count'] = data
          case "Material2_Id":
            if data != "None":
              item.recipe['mat2_id'] = item_names["ITEM_NAME_"+data]['TextData']['LocalizedString']
          case "Material2_Count":
            if data != 0:
              item.recipe['mat2_count'] = data
          case "Material3_Id":
            if data != "None":
              item.recipe['mat3_id'] = item_names["ITEM_NAME_"+data]['TextData']['LocalizedString']
          case "Material3_Count":
            if data != 0:
              item.recipe['mat3_count'] = data
          case "Material4_Id":
            if data != "None":
              item.recipe['mat4_id'] = item_names["ITEM_NAME_"+data]['TextData']['LocalizedString']
          case "Material4_Count":
            if data != 0:
              item.recipe['mat4_count'] = data
          case "Material5_Id":
            if data != "None":
              item.recipe['mat5_id'] = item_names["ITEM_NAME_"+data]['TextData']['LocalizedString']
          case "Material5_Count":
            if data != 0:
              item.recipe['mat5_count'] = data
          case "Product_Count":
            item.recipe['count'] = data
    except KeyError:
      print(f"No recipe for {item_name} found")
    
    item_list.append(asdict(item))

  return item_list

def make_item_table(item_list: dict) -> str:
    
    sorted_list = sorted(item_list, key=lambda x: x['name'])

    table = f"""{{| class="wikitable sortable mw-collapsible"
|+
!Item
!Category
!Rarity
!Consumable?
!Weight
!Durability
!Buy Price
!Sell Price
!Mag Size
!Armor HP
!Armor Def
!Shield Value
"""
    for item in sorted_list:
      entry = f"""|-
|{{{{i|{item['name']}}}}}
|[[{item['item_type']}]]
|{str(item['rarity'])}
|{str(item['consumable'])}
|{str(item['weight'])}
|{str(item['durability'])}
|{str(item['buy_price'])}
|{str(item['sell_price'])}
|{str(item['mag_size'])}
|{str(item['armor_hp'])}
|{str(item['armor_def'])}
|{str(item['shield_value'])}
"""
      table += entry
    
    table += "|}\n"

    return table

def main():
  
  items = get_items()
  print(json.dumps(items))

if __name__ == "__main__":
  main()