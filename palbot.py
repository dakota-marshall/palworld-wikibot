import pywikibot
import json
import argparse
import re
from pywikibot import pagegenerators
from pywikibot.bot import SingleSiteBot
from src.suitability_parser import get_suitabilities
from src.partner_skill_parser import get_partner_skills
from src.item_parser import get_items

class PalworldBot(SingleSiteBot):
  """Main bot class for the Palworld Wiki"""

  def get_watering_page(self) -> str:
    """Gets text from the Watering page, mainly used as connection test"""
    #Load the watering page and grab text
    text = pywikibot.Page(self.site, "Watering").text

    return text
  
  def gen_partner_skills(self) -> None:
    """Generate the partner skill data and uplodat to Module:PartnerSkills/data.json"""
    partner_skill_page: pywikibot.Page = pywikibot.Page(self.site, "Module:PartnerSkills/data.json")

    partner_skills = json.dumps(get_partner_skills(), indent=4)

    partner_skill_page.text = partner_skills
    partner_skill_page.save('Update Partner Skill Data')

  def gen_suitability_tables(self) -> None:
    """Generates the suitability data using the parser, and uploads that data to Module:WorkSuitabilities/data.json"""

    suitability_page: pywikibot.Page = pywikibot.Page(self.site, "Module:WorkSuitabilities/data.json")

    suitabilities = json.dumps(get_suitabilities(), indent=4)

    suitability_page.text = suitabilities
    suitability_page.save('Update suitability data')
  
  def gen_items(self) -> None:
    """Generate and upload all item data to Module:Items/data.json"""
    
    items_page: pywikibot.Page = pywikibot.Page(self.site, "Module:Items/data.json")

    items = json.dumps(get_items(), indent=4)

    items_page.text = items
    items_page.save('Update suitability data')
  
  def update_item_pages(self) -> None:
    """Updates all item pages with Item Data"""

    items = get_items()
    templates = []

    for item in items:
      print(f"Updating page for {item['name']}?")
      page: pywikibot.Page = pywikibot.Page(self.site, f"{item['name'].replace(' ', '_')}")

      original_text = page.text

      # Generate Template
      newline = "\r\n"
      template = f"""{{{{Item
| description   = {item['description'].replace(newline, ' ')}
| type          = [[{item['item_type']}]]
| rarity        = {item['rarity']}
| consumable    = {item['consumable']}

| weight        = {item['weight']}
| durability    = {item['durability'] if item['durability'] > 0 else ""}

| buy           = {{{{i|Gold Coin|notext}}}}{item['buy_price']}
| sell          = {{{{i|Gold Coin|notext}}}}{item['sell_price']}

| combat        = {any(val > 0 for val in [item['mag_size'], item['attack']]) or ""}
| hp            = 
| capture_power = 
| magazine      = {item['mag_size'] if item['mag_size'] > 0 else ""}
| attack        = {item['attack'] if item['attack'] > 0 else ""}

| defense       = {any(val > 0 for val in [item['armor_def'], item['armor_hp'], item['shield_value']]) or ""}
| armor_defense = {item['armor_def'] if item['armor_def'] > 0 else ""}
| armor_health  = {item['armor_hp'] if item['armor_hp'] > 0 else ""}
| shield        = {item['shield_value'] if item['shield_value'] > 0 else ""}
| equip_effect  =

| glider_speed  = 
| glider_drain  = 

| food          = 
| nutrition     = 
| san           = 

| technology    = 
| required_level = 
| cost          = 
| made_at       = 
}}}}"""

      # Update Page
      if "{{Item" in page.text:
        print("Updating existing page...")
        match = re.search(r'\{\{Item.*?\n\}\}', page.text, re.DOTALL)
        if template != match:
          page.text = page.text.replace(match.group(0), template)
      else:
        # Create new page
        print("Creating new page")
        page.text = "{{stub}}"
        page.text += template

      # Add recipe
      if item['recipe']:
        recipe_text = f"""{{{{Recipe
{("|mat1="+str(item['recipe']['mat1_id'])) if "mat1_id" in item['recipe'].keys() else ""}
{("|mat1qty="+str(item['recipe']['mat1_count'])) if "mat1_count" in item['recipe'].keys() else ""}
{("|mat2="+str(item['recipe']['mat2_id'])) if "mat2_id" in item['recipe'].keys() else ""}
{("|mat2qty="+str(item['recipe']['mat2_count'])) if "mat2_count" in item['recipe'].keys() else ""}
{("|mat3="+str(item['recipe']['mat3_id'])) if "mat3_id" in item['recipe'].keys() else ""}
{("|mat3qty="+str(item['recipe']['mat3_count'])) if "mat3_count" in item['recipe'].keys() else ""}
{("|mat4="+str(item['recipe']['mat4_id'])) if "mat4_id" in item['recipe'].keys() else ""}
{("|mat4qty="+str(item['recipe']['mat4_count'])) if "mat4_count" in item['recipe'].keys() else ""}
{("|mat5="+str(item['recipe']['mat5_id'])) if "mat5_id" in item['recipe'].keys() else ""}
{("|mat5qty="+str(item['recipe']['mat5_count'])) if "mat5_count" in item['recipe'].keys() else ""}
{("|output1="+item['name']) if "mat1_id" in item['recipe'].keys() else ""}
{("|output1qty="+str(item['recipe']['count'])) if "count" in item['recipe'].keys() else ""}
}}}}
"""

        if "{{Recipe" in page.text:
          match = re.search(r'\{\{Recipe.*?\n\}\}', page.text, re.DOTALL)
          page.text = page.text.replace(match.group(0), recipe_text)
        else:
          page.text += "\n==Crafting=="
          page.text += "\n" + recipe_text
      

      page.save("update infobox from dumped data")
  
def parse_arguments() -> argparse.Namespace:

  # Start the parser
  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers(dest='command')

  # Gen Suitability
  suitability = subparsers.add_parser('gen_suitability', help='Generate and Upload Suitability data')

  # Get Category Parser
  category = subparsers.add_parser('test', help='Get all pages of provided category')

  # Partner skills
  partner_skills = subparsers.add_parser('gen_partner_skills', help='Generate and Upload partner skill data')

  # Items
  items = subparsers.add_parser('items', help='Work with item data')
  items.add_argument("item_command",
                     choices=["get_items", "update_pages"]
                     )

  # Parse
  args = parser.parse_args()

  return args

def main() -> None:

  #Instantiate bot
  bot: PalworldBot = PalworldBot()

  args = parse_arguments()

  # Run the appropriate command based on args
  match args.command:
    case 'test':
      text = bot.get_watering_page()
      print(text)
    case 'gen_suitability':
      bot.gen_suitability_tables()
    case 'gen_partner_skills':
      bot.gen_partner_skills()
    case 'items':
      match args.item_command:
        case 'get_items':
          bot.gen_items()
        case 'update_pages':
          bot.update_item_pages()

if __name__ == "__main__":
  main()