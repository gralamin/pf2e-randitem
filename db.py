import os
import json

__curdir__ = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(__curdir__, "pf2e/packs/equipment/")

db = {"consumable": [], "permenant": []}
all_traits = set()


def load_db_folder(path):
    for root, dirs, files in os.walk(path):
        for name in files:
            filepath = os.path.join(path, name)
            with open(filepath, "r") as f:
                cur_data = json.load(f)
                key = (
                    "consumable"
                    if "consumable" in cur_data["system"]["traits"]["value"]
                    # Wands are randomly listed as consumable for no apparent reason
                    or (
                        cur_data["type"] == "consumable"
                        and "wand" not in cur_data["system"]["traits"]["value"]
                    )
                    else "permenant"
                )
                all_traits.update(set(cur_data["system"]["traits"]["value"]))
                all_traits.add(cur_data["type"])
                db[key].append(cur_data)
                cur_data["system"].setdefault("usage", {"value": "foo"})
                cur_data["system"].setdefault("level", {"value": 0})
        for name in dirs:
            load_db_folder(os.path.join(path, name))


def load_db(custom_db):
    load_db_folder(path)
    if custom_db:
        load_db_folder(custom_db)
    # check usage value contains "held" for held items
    all_traits.add("held")
    # check usage value contains "etched" for runes
    all_traits.add("etched")
    # Check usage value contains "worn" for worn items
    all_traits.add("worn")
    # Special trait for things without for filtering
    all_traits.add("none")
    # Special case consumable, saids to just reroll ignoring formula
    all_traits.add("formula")
    # Special case for magical ammo
    all_traits.add("ammo")


db_used_trait_list = set(
    [
        "adjustment",
        "alchemical",
        "ammo",
        "apex",
        "armor",
        "catalyst",
        "contract",
        "cursed",
        "etched",
        "formula",
        "fulu",
        "gadget",
        "grimoire",
        "held",
        "intelligent",
        "missive",
        "none",
        "oil",
        "potion",
        "precious",
        "scroll",
        "snare",
        "spellheart",
        "staff",
        "structure",
        "talisman",
        "tattoo",
        "tech",
        "wand",
        "weapon",
        "worn",
    ]
)
