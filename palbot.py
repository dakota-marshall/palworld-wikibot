import pywikibot
import json
import argparse
from pywikibot import pagegenerators
from pywikibot.bot import SingleSiteBot
from src.suitability_parser import get_suitabilities
from src.partner_skill_parser import get_partner_skills

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


if __name__ == "__main__":
  main()