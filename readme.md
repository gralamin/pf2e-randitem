From the pf2e subfolder, get the items from:  pf2e/packs/data/equipment.db/
Load each json file into memory
Reference the type table to determine which options to check
Filter the options by the level we are generating
Filter by traits -> value -> consumable
If there is no results, reroll one level up, and mark the node as visited
If no nodes are unvisited, reroll one level up.
If all nodes are visited return error