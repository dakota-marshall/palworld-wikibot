import pywikibot
import json
import argparse
from pywikibot import pagegenerators
from pywikibot.bot import SingleSiteBot
from src.suitability_parser import get_suitabilities

class PalworldBot(SingleSiteBot):
  """Main bot class for the Palworld Wiki"""

  def get_watering_page(self) -> str:
    """Gets text from the Watering page, mainly used as connection test"""
    #Load the watering page and grab text
    text = pywikibot.Page(self.site, "Watering").text

    return text
  
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



  

if __name__ == "__main__":
  main()