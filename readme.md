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
usage: generate.py [-h] -l LEVEL [-c]
                   [-t {adjustment,alchemical,ammo,apex,armor,catalyst,contract,cursed,etched,formula,fulu,gadget,grimoire,held,intelligent,missive,none,oil,potion,precious,scroll,snare,spellheart,staff,structure,talisman,tattoo,tech,wand,weapon,worn}]
                   [-u CUSTOM_DB] [-s SEED]
                   [-i {adjustment,alchemical,ammo,apex,armor,catalyst,contract,cursed,etched,formula,fulu,gadget,grimoire,held,intelligent,missive,none,oil,potion,precious,scroll,snare,spellheart,staff,structure,talisman,tattoo,tech,wand,weapon,worn}]
                   [-r]

optional arguments:
  -h, --help            show this help message and exit
  -l LEVEL, --level LEVEL
  -c, --consumable
  -t {adjustment,alchemical,ammo,apex,armor,catalyst,contract,cursed,etched,formula,fulu,gadget,grimoire,held,intelligent,missive,none,oil,potion,precious,scroll,snare,spellheart,staff,structure,talisman,tattoo,tech,wand,weapon,worn}, --trait {adjustment,alchemical,ammo,apex,armor,catalyst,contract,cursed,etched,formula,fulu,gadget,grimoire,held,intelligent,missive,none,oil,potion,precious,scroll,snare,spellheart,staff,structure,talisman,tattoo,tech,wand,weapon,worn}
                        Force this trait or type to appear
  -u CUSTOM_DB, --custom-db CUSTOM_DB
                        Custom db path to load
  -s SEED, --seed SEED
  -i {adjustment,alchemical,ammo,apex,armor,catalyst,contract,cursed,etched,formula,fulu,gadget,grimoire,held,intelligent,missive,none,oil,potion,precious,scroll,snare,spellheart,staff,structure,talisman,tattoo,tech,wand,weapon,worn}, --ignore {adjustment,alchemical,ammo,apex,armor,catalyst,contract,cursed,etched,formula,fulu,gadget,grimoire,held,intelligent,missive,none,oil,potion,precious,scroll,snare,spellheart,staff,structure,talisman,tattoo,tech,wand,weapon,worn}
                        Ignore traits, eg '-i tattoo -i wand' will prevent tattoos and wands from being generated
  -r, --report          If specified, instead of generating an item, list out effective probabilities of each item,
                        and the trait they are associated with.
```

To expand slightly:
* `level` is the item level, you are generally generating an item of a certain level
* `consumable` is pretty self explainatory, the rules suggest a certain number of permenant items and consumables. If this is specified, it will be a consumable. If not, it will not be.
* `trait` allows you to force a certain trait to be generated from the given list. Note that I make each item only appear under one of these traits, and it might not be intunitive to you. The logic for this can be found in `generate.py` in `find_possibility_from_trait`.
* `custom-db` allows ADDING custom items by specifying them in a custom_db, see `custom_db/test_custom.json` for an example. Note due to assumptions its possible these will be more likely based on certain words. The test exploits this to make it more likely to show up by pretending to be a `resilient` armor rune.
* `seed` Random seed for debugging / reproducing a result
* `ignore` will make an item grouped in a certain trait not be generated. This can be useful if you generated a `formula`.
* `report` will skip generation and show a report of the probability of each item of that level / consumable, and what trait its under.

To generate a level 9 consumable:
```
$ generate.py -l 9 -c
Ixamè's Eye - trait criteria: talisman
Seed 4344469498447680552
```

If you can't generate an item (for example, you have ignored all valid categories for the level), a value error will be thrown:
```
$ python generate.py -l 1 -i none -i armor -i held -i weapon -i worn -i tattoo -i adjustment
Traceback (most recent call last):
  File "generate.py", line 353, in <module>
    main()
  File "generate.py", line 319, in main
    trait, choice = generate_permenant(key, level, args.trait, args.ignore)
  File "generate.py", line 336, in generate_permenant
    trait, choice = generate_from_table(db.db, possible_traits, key, level, False)
  File "generate.py", line 15, in generate_from_table
    raise ValueError("Failed to generate item")
ValueError: Failed to generate item
```

You can generate a report pretty simply:
```
$ python generate.py -l 1 -c -r
{'Ablative Armor Plating (Lesser)': {'p': '0.25%', 'trait': 'gadget'},
 'Ablative Shield Plating (Lesser)': {'p': '0.25%', 'trait': 'gadget'},
 'Acid Flask (Lesser)': {'p': '0.25%', 'trait': 'alchemical'},
 'Addiction Suppressant (Lesser)': {'p': '0.25%', 'trait': 'alchemical'},
 'Alarm Snare': {'p': '0.27%', 'trait': 'snare'},
 'Alchemical Fuse': {'p': '0.25%', 'trait': 'alchemical'},
 "Alchemist's Fire (Lesser)": {'p': '0.25%', 'trait': 'alchemical'},
 'Alignment Ampoule (Lesser)': {'p': '0.25%', 'trait': 'alchemical'},
 ...
```

Report works with the other options, so you can see exactly what you are trying to do:
```
$ python generate.py -l 1 -c -r -i alchemical -i snare -i talisman -i potion -i held -i ammo -i formula -i oil -i catalyst
{'Ablative Armor Plating (Lesser)': {'p': '0.96%', 'trait': 'gadget'},
 'Ablative Shield Plating (Lesser)': {'p': '0.96%', 'trait': 'gadget'},
 'Blast Boots (Lesser)': {'p': '0.96%', 'trait': 'gadget'},
 'Clockwork Goggles': {'p': '0.96%', 'trait': 'gadget'},
 'Cryomister (Lesser)': {'p': '0.96%', 'trait': 'gadget'},
 'Explosive Mine (Lesser)': {'p': '0.96%', 'trait': 'gadget'},
 'Flare Beacon (Lesser)': {'p': '0.96%', 'trait': 'gadget'},
 'Impact Foam Chassis (Lesser)': {'p': '0.96%', 'trait': 'gadget'},
 'Scroll of 1st-level Spell': {'p': '73.08%', 'trait': 'scroll'}}
```

## For development
1. Test with generate_int_test.py
2. Format with format.sh (assumes a virtual env has been made in this folder called v, and installed black)