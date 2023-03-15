import random
import argparse
import sys

import db


def generate_from_table(db, possible_traits, key, level, is_consumable):
    visited_traits = set()
    found = None
    while found is None:
        choosen_trait = None
        possible_traits = [x for x in possible_traits if x not in visited_traits]
        if not possible_traits:
            raise ValueError("Failed to generate item")
        choosen_trait = random.choice(possible_traits)
        visited_traits.add(choosen_trait)
        possibilities = find_possibility_from_trait(
            db, choosen_trait, key, level, is_consumable
        )
        if possibilities:
            found = random.choice(possibilities)
    return choosen_trait, found


def find_possibility_from_trait(db, choosen_trait, key, level, is_consumable):
    by_level = [
        x for x in db[key] if x["system"].get("level", {"value": 0})["value"] == level
    ]
    # some items have multiple traits, trait order first.
    claimed_items = set()

    # Cursed supersecedes all
    cursed_items = [
        x
        for x in by_level
        if "cursed" in x["system"]["traits"]["value"] and x["name"] not in claimed_items
    ]
    claimed_items.update(x["name"] for x in cursed_items)

    # ammo, staff, tech, weapon and armor is generated with some special cases
    # Staffs are also weapons sometimes, but I want them in staff.
    staff_items = [
        x
        for x in by_level
        if "staff" in x["system"]["traits"]["value"] and x["name"] not in claimed_items
    ]
    claimed_items.update(x["name"] for x in staff_items)
    # tech are weapons, but shoulld be rarer as they are "hi tech"
    tech_items = [
        x
        for x in by_level
        if "tech" in x["system"]["traits"]["value"] and x["name"] not in claimed_items
    ]
    claimed_items.update(x["name"] for x in tech_items)

    # bomb workaround
    if not is_consumable:
        # Permenant items first
        weapon_items = [
            x
            for x in by_level
            if "weapon" in x["system"]["traits"]["value"]
            or x["type"] == "weapon"
            and x["name"] not in claimed_items
        ]
        claimed_items.update(x["name"] for x in weapon_items)

        armor_items = [
            x
            for x in by_level
            if "armor" in x["system"]["traits"]["value"]
            or x["type"] == "armor"
            and x["name"] not in claimed_items
        ]
        claimed_items.update(x["name"] for x in armor_items)
    else:
        weapon_items = []
        armor_items = []

    ammo_items = [
        x
        for x in by_level
        if x["system"].get("consumableType", {"value": "junk"})["value"] == "ammo"
        and x["name"] not in claimed_items
    ]
    claimed_items.update(x["name"] for x in ammo_items)

    claimed_traits = {
        "cursed": cursed_items,
        "weapon": weapon_items,
        "armor": armor_items,
        "ammo": ammo_items,
        "staff": staff_items,
        "tech": tech_items,
    }

    # This list order defines precedence
    for trait in [
        "intelligent",
        "apex",
        "adjustment",
        "contract",
        "scroll",
        "catalyst",
        "gadget",
        "alchemical",
        "oil",
        "potion",
        "snare",
        "fulu",
        "talisman",
        "missive",
        "precious",
        "spellheart",
        "grimoire",
        "structure",
        "wand",
    ]:
        # structure also shouldn't be grabbed for consumable
        if trait == "structure" and is_consumable:
            continue
        items = [
            x
            for x in by_level
            if trait in x["system"]["traits"]["value"]
            and x["name"] not in claimed_items
        ]
        claimed_items.update(x["name"] for x in items)
        claimed_traits[trait] = items

    # Held, claimed, and etched are also special
    held_items = [
        x
        for x in by_level
        if (
            "held" in x["system"]["usage"]["value"]
            or "touched" in x["system"]["usage"]["value"]
            or "other" in x["system"]["usage"]["value"]
        )
        and x["name"] not in claimed_items
    ]
    claimed_items.update(x["name"] for x in held_items)
    worn_items = [
        x
        for x in by_level
        if "worn" in x["system"]["usage"]["value"] and x["name"] not in claimed_items
    ]
    claimed_items.update(x["name"] for x in worn_items)

    etched_items = [
        x
        for x in by_level
        if "etched" in x["system"]["usage"]["value"]
        or "applied" in x["system"]["usage"]["value"]
        and x["name"] not in claimed_items
    ]
    claimed_items.update(x["name"] for x in etched_items)

    # Make some etchings more likely
    # If we want these to be half the end list, then we want to add:
    # Number of items in the list - 2
    # If you think about it, the Match cancels out one non match
    # so to get to half, you add the number of elements left.
    special_etched_number = len(etched_items) - 2 if len(etched_items) >= 2 else 0
    for x in list(etched_items):
        if (
            "Weapon Potency" in x["name"]
            or "Armor Potency" in x["name"]
            or "Striking" in x["name"]
            or "Resilient" in x["name"]
        ):
            # Make basic potency more likely
            for _ in range(special_etched_number):
                etched_items.append(x)

    claimed_traits["held"] = held_items
    claimed_traits["worn"] = worn_items
    claimed_traits["etched"] = etched_items

    if choosen_trait == "none":
        possible_items = [x for x in by_level if x["name"] not in claimed_items]
        if is_consumable:
            return [
                x
                for x in possible_items
                if len(x["system"]["traits"]["value"]) == 1
                and "consumable" in x["system"]["traits"]["value"]
            ]
        return [
            x
            for x in possible_items
            if len(x["system"]["traits"]["value"]) == 0
            or "attached" in x["system"]["usage"]["value"]
            or "affixed" in x["system"]["usage"]["value"]
        ]
    elif choosen_trait == "formula":
        return [
            {"name": "Formula: Ritual"},
            {"name": "Formula: Permanent Item (Reroll without -c)"},
            {"name": "Formula: Permanent Item (Reroll without -c)"},
            {"name": "Formula: Permanent Item (Reroll without -c)"},
            {"name": "Formula: Consumable (Reroll ignoring formula results)"},
            {"name": "Formula: Consumable (Reroll ignoring formula results)"},
        ]
    elif choosen_trait in claimed_traits:
        return claimed_traits[choosen_trait]
    else:
        return [
            x
            for x in by_level
            if choosen_trait in x["system"]["traits"]["value"]
            or x["type"] == choosen_trait
            and x["name"] not in claimed_items
        ]


def generate_possible_list(all_traits, chance_dict):
    l = [
        item
        for sublist in [[key] * value for key, value in chance_dict.items()]
        for item in sublist
    ]
    unknown = set(x for x in l if x not in all_traits)
    assert len(unknown) == 0, "Unknown traits: {}".format(unknown)
    return l


def permenant_list():
    # none is [adventuring gear, animals, assistive items, constuomization, trade goods, vehicles]
    # armor is armor and shields
    # Held contains other
    # Etched is much higher to represent both armor and weapon potency.
    # It has stolen 6 from armor and 6 from weapon
    return generate_possible_list(
        db.db_used_trait_list,
        {
            "cursed": 1,
            "alchemical": 1,
            "adjustment": 1,
            "none": 2 + 1 + 1 + 1 + 1 + 1,
            "apex": 5,
            "armor": 10 + 7 - 6,
            "contract": 2,
            "grimoire": 5,
            "held": 10 + 1,
            "tech": 1,
            "intelligent": 1,
            "precious": 1,
            "etched": 10 + 6 + 6,
            "spellheart": 3,
            "staff": 6,
            "structure": 1,
            "tattoo": 2,
            "wand": 5,
            "weapon": 10 - 6,
            "worn": 10,
        },
    )


def consumable_list():
    return generate_possible_list(
        db.db_used_trait_list,
        {
            "cursed": 1,
            "formula": 19,
            "alchemical": 19,
            "fulu": 1,
            "none": 1,
            "gadget": 2,
            "ammo": 2,
            "missive": 1,
            "oil": 5,
            "potion": 3,
            "scroll": 19,
            "catalyst": 2,
            "talisman": 19,
            "snare": 3,
            # held and worn covers "other consumables" here.
            "held": 2,
            "worn": 1,
        },
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--level", type=int, required=True)
    parser.add_argument("-c", "--consumable", action="store_true")
    parser.add_argument(
        "-t",
        "--trait",
        help="Force this trait or type to appear",
        choices=sorted(db.db_used_trait_list),
    )
    parser.add_argument(
        "-u",
        "--custom-db",
        type=str,
        help="Custom db path to load",
        default=None,
    )
    parser.add_argument("-s", "--seed", type=int, default=None)
    args = parser.parse_args()
    level = args.level
    is_consumable = args.consumable
    seed = random.randrange(sys.maxsize) if not args.seed else args.seed
    random.seed(seed)

    db.load_db(args.custom_db)

    key = "consumable" if is_consumable else "permenant"
    if is_consumable:
        trait, choice = generate_consumable(key, level, args.trait)
    else:
        trait, choice = generate_permenant(key, level, args.trait)

    if "name" in choice:
        print("{} - trait criteria: {}".format(choice["name"], trait))
    else:
        print("{} - trait criteria: {}".format(choice, trait))
    print("Seed {}".format(seed))


def generate_permenant(key, level, trait=None):
    if trait == None:
        possible_traits = permenant_list()
        assert len(possible_traits) == 100
    else:
        possible_traits = [trait]
    trait, choice = generate_from_table(db.db, possible_traits, key, level, False)
    return trait, choice


def generate_consumable(key, level, trait=None):
    if trait == None:
        possible_traits = consumable_list()
        assert len(possible_traits) == 100
    else:
        possible_traits = [trait]
    trait, choice = generate_from_table(db.db, possible_traits, key, level, True)
    return trait, choice


if __name__ == "__main__":
    main()
