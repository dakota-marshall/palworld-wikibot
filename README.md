# Palworld Wiki Bot

Bot used to populate data in the [Palworld Wiki](https://palworld.wiki.gg) from game data dumps.

## Prerequisites

It is assumed that you have the game data dumps available inside the `data/` folder. These can be retrieved from the [Palworld Wiki Discord](https://discord.gg/kQswWFm5g6)

## Setup

- Install `pywikibot` (See [here](https://www.mediawiki.org/wiki/Manual:Pywikibot/Installation) for advanced configuration)

```bash
pip install pywikibot
```

- Fill in your user credentials in `user-config.py`
- Login to the wiki

```bash
pwb login
```

## Usage

```bash
./palbot.py $command
```

### Current Accepted Commands

```
usage: palbot.py [-h] {gen_suitability,test} ...

positional arguments:
  {gen_suitability,test}
    gen_suitability     Generate and Upload Suitability data
    test                Get all pages of provided category

options:
  -h, --help            show this help message and exit
```

## Adding Scripts

If you would like to add a script to this, you can add the file into the `src/` directory, and write the function that does the parsing you want to accomplish You can then go into the `palworld.py` bot and add the following:

- Import the function
- Add a method to the `PalWorldBot` class that runs your parser, and uploads the changes to the wiki
- Add a command to the `parse_arguments()`, and a `case` to the match block in the `main()` function to call your method when the command matches

### Passing extra arguments

If you want users to be able to pass extra arguments to your method, you can add the following to your piece of the argument parser:

```python
example_parser = subparser.add_parser('example', help="Example command with extra args")
example_parser.add_argument('--test', '-t', dest='test', help='extra arg created with "example"')
```

You can then pass that argument to your method, accessible at `args.test`:
```python
match args.command:
  case 'example':
    bot.my_example_method(args.test)
```