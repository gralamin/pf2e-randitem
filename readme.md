# Pathfinder 2e random item generator

This is a pathfinder 2e random item generator, with weighting applied to make certain item types (such as scrolls), more likely.

The weighting is in `generate.py` in the `consumable_list` and `permenant_list` functions. I could move it to a json file, but it feels like overkill.

Currently the weighting is forced to add up to 100, this is to make it possible to reproduce with a d100.

## Prerequistes
1. Clone https://github.com/foundryvtt/pf2e.git into the folder
2. Python 3

## To run
Simply run with python3 against generate.py

```
$ usage: generate.py [-h] -l LEVEL [-c]
                   [-t {adjustment,alchemical,ammo,apex,armor,catalyst,contract,cursed,etched,formula,fulu,gadget,grimoire,held,intelligent,missive,none,oil,potion,precious,scroll,snare,spellheart,staff,structure,talisman,tattoo,tech,wand,weapon,worn}]
                   [-u CUSTOM_DB] [-s SEED]

optional arguments:
  -h, --help            show this help message and exit
  -l LEVEL, --level LEVEL
  -c, --consumable
  -t {adjustment,alchemical,ammo,apex,armor,catalyst,contract,cursed,etched,formula,fulu,gadget,grimoire,held,intelligent,missive,none,oil,potion,precious,scroll,snare,spellheart,staff,structure,talisman,tattoo,tech,wand,weapon,worn}, --trait {adjustment,alchemical,ammo,apex,armor,catalyst,contract,cursed,etched,formula,fulu,gadget,grimoire,held,intelligent,missive,none,oil,potion,precious,scroll,snare,spellheart,staff,structure,talisman,tattoo,tech,wand,weapon,worn}
                        Force this trait or type to appear
  -u CUSTOM_DB, --custom-db CUSTOM_DB
                        Custom db path to load
  -s SEED, --seed SEED
```

To expand slightly:
* `level` is the item level, you are generally generating an item of a certain level
* `consumable` is pretty self explainatory, the rules suggest a certain number of permenant items and consumables. If this is specified, it will be a consumable. If not, it will not be.
* `trait` allows you to force a certain trait to be generated from the given list. Note that I make each item only appear under one of these traits, and it might not be intunitive to you. The logic for this can be found in `generate.py` in `find_possibility_from_trait`.
* `custom-db` allows ADDING custom items by specifying them in a custom_db, see `custom_db/test_custom.json` for an example. Note due to assumptions its possible these will be more likely based on certain words. The test exploits this to make it more likely to show up by pretending to be a `resilient` armor rune.
* `seed` Random seed for debugging / reproducing a result

So to generate a level 9 consumable:
```
$ generate.py -l 9 -c
Ixamè's Eye - trait criteria: talisman
Seed 4344469498447680552
```

## For development
1. Test with generate_int_test.py
2. Format with format.sh (assumes a virtual env has been made in this folder called v, and installed black)

## Features to add:
1. Add a feature that prints out what the chance of rolling each item of a given level ends up being. Note this will vary by item.
2. Add an "Ignore" feature that lets you ignore one or more traits.