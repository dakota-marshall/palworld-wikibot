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