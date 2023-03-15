# integration test for generation
# The goal here is to check that each trait is generating a unique list of items
# and all items are reached

import unittest

import db
import generate

db.load_db(custom_db=None)
max_level = max([x["system"]["level"]["value"] for x in db.db["permenant"]])


class TestIntegration(unittest.TestCase):
    def test_permenant_seen(self):
        key = "permenant"
        subdb = db.db[key]
        all_items = set(x["name"] for x in subdb)
        # Class kits shouldn't be generated
        seen_items = set(
            [
                "Class Kit (Alchemist)",
                "Class Kit (Barbarian)",
                "Class Kit (Bard)",
                "Class Kit (Champion)",
                "Class Kit (Cleric)",
                "Class Kit (Druid)",
                "Class Kit (Fighter)",
                "Class Kit (Investigator)",
                "Class Kit (Monk)",
                "Class Kit (Oracle)",
                "Class Kit (Ranger)",
                "Class Kit (Rogue)",
                "Class Kit (Sorcerer)",
                "Class Kit (Swashbuckler)",
                "Class Kit (Witch)",
                "Class Kit (Wizard)",
            ]
        )
        # Artifacts shouldn't be generated
        seen_items.update(
            [x["name"] for x in subdb if "artifact" in x["system"]["traits"]["value"]]
        )
        for level in range(0, max_level):
            for trait in generate.permenant_list():
                possibilities = generate.find_possibility_from_trait(
                    db.db, trait, key, level, False
                )
                new_items = set(x["name"] for x in possibilities)
                seen_items.update(new_items)
        missing_items = all_items - seen_items
        self.assertEqual(len(missing_items), 0, sorted(missing_items))

    def test_consumable_seen(self):
        key = "consumable"
        subdb = db.db[key]
        all_items = set(x["name"] for x in subdb)
        seen_items = set()
        for level in range(0, max_level):
            for trait in generate.consumable_list():
                possibilities = generate.find_possibility_from_trait(
                    db.db, trait, key, level, True
                )
                new_items = set(x["name"] for x in possibilities)
                seen_items.update(new_items)
        missing_items = all_items - seen_items
        self.assertEqual(len(missing_items), 0, missing_items)

    def test_consumable_unique(self):
        key = "consumable"
        debug = False
        seen_items = set()
        traits = sorted(set(generate.consumable_list()))
        for level in range(0, max_level):
            if debug:
                print("\n\nLevel: {}".format(level))
            for trait in traits:
                if debug:
                    print("\t trait: {}".format(trait))
                if "formula" == trait:
                    # skip formulas
                    continue
                possibilities = generate.find_possibility_from_trait(
                    db.db, trait, key, level, True
                )
                new_items = set(x["name"] for x in possibilities)
                duplicates = [x for x in new_items if x in seen_items]
                self.assertEqual(
                    len(duplicates),
                    0,
                    "Duplicates found at level: {}, trait: {}. duplicates: {}".format(
                        level, trait, sorted(duplicates)
                    ),
                )
                if debug:
                    print("Adding {}".format(sorted(new_items)))
                seen_items.update(new_items)

    def test_permenant_unique(self):
        key = "permenant"
        debug = False
        seen_items = set()
        traits = sorted(set(generate.permenant_list()))
        for level in range(0, max_level):
            if debug:
                print("\n\nLevel: {}".format(level))
            for trait in traits:
                if debug:
                    print("\t trait: {}".format(trait))
                if "formula" == trait:
                    # skip formulas
                    continue
                possibilities = generate.find_possibility_from_trait(
                    db.db, trait, key, level, False
                )
                new_items = set(x["name"] for x in possibilities)
                duplicates = [x for x in new_items if x in seen_items]
                self.assertEqual(
                    len(duplicates),
                    0,
                    "Duplicates found at level: {}, trait: {}. duplicates: {}".format(
                        level, trait, sorted(duplicates)
                    ),
                )
                if debug:
                    print("Adding {}".format(sorted(new_items)))
                seen_items.update(new_items)


if __name__ == "__main__":
    unittest.main()
