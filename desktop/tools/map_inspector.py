#!/usr/bin/env python3
"""
Map Data Inspector CLI Tool
Inspect game map data: locations, NPCs, encounters, transitions, dungeons
"""

import os
import sys
import argparse

# CRITICAL: Set SDL_VIDEODRIVER before any pygame/game imports
os.environ['SDL_VIDEODRIVER'] = 'dummy'

# Set up sys.path to find shim and game modules
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
shim_dir = os.path.join(project_root, 'desktop', 'shim')

sys.path.insert(0, shim_dir)
sys.path.insert(1, project_root)

# Now safe to import game modules
from data.locations import LOCATIONS, LOCATION_NPCS, LOCATION_TRIGGERS
from data.dungeons import DUNGEONS
from data.npcs import NPCS


def list_locations():
    """List all locations with ID, name, and fast travel status"""
    print("\n=== All Locations ===\n")
    print(f"{'ID':<30} {'Name':<35} {'Fast Travel':<12} {'Encounter Rate'}")
    print("-" * 90)

    for loc_id, loc_data in sorted(LOCATIONS.items()):
        name = loc_data.get('name', 'Unknown')
        fast_travel = "Yes" if loc_data.get('fast_travel', False) else "No"
        encounter_rate = loc_data.get('encounter_rate', 0.0)
        print(f"{loc_id:<30} {name:<35} {fast_travel:<12} {encounter_rate:.2f}")

    print(f"\nTotal locations: {len(LOCATIONS)}\n")


def show_location_details(location_name):
    """Show detailed properties for a single location"""
    # Try exact match first
    loc_id = location_name
    if loc_id not in LOCATIONS:
        # Try case-insensitive search
        matches = [lid for lid in LOCATIONS.keys() if lid.lower() == location_name.lower()]
        if matches:
            loc_id = matches[0]
        else:
            print(f"\nError: Location '{location_name}' not found.")
            print("Use --list to see all available locations.\n")
            return

    loc = LOCATIONS[loc_id]
    print(f"\n=== Location: {loc.get('name', 'Unknown')} ===\n")
    print(f"ID:               {loc_id}")
    print(f"Description:      {loc.get('description', 'N/A')}")
    print(f"Spawn Position:   {loc.get('spawn_position', 'N/A')}")
    print(f"Fast Travel:      {'Yes' if loc.get('fast_travel', False) else 'No'}")
    print(f"Encounter Rate:   {loc.get('encounter_rate', 0.0):.2f}")

    if 'encounter_table' in loc:
        print(f"Encounter Table:  {loc['encounter_table']}")

    if 'requires_flag' in loc:
        print(f"Requires Flag:    {loc['requires_flag']}")

    if 'parent_location' in loc:
        print(f"Parent Location:  {loc['parent_location']}")

    print()


def show_location_npcs(location_name):
    """Show NPCs at a location"""
    # Try exact match first
    loc_id = location_name
    if loc_id not in LOCATIONS:
        # Try case-insensitive search
        matches = [lid for lid in LOCATIONS.keys() if lid.lower() == location_name.lower()]
        if matches:
            loc_id = matches[0]
        else:
            print(f"\nError: Location '{location_name}' not found.")
            return

    npcs = LOCATION_NPCS.get(loc_id, {})

    print(f"\n=== NPCs at {LOCATIONS[loc_id].get('name', loc_id)} ===\n")

    if not npcs:
        print("No NPCs at this location.\n")
        return

    print(f"{'NPC ID':<25} {'Name':<20} {'Position':<15} {'Dialogue':<20} {'Shop'}")
    print("-" * 100)

    for npc_id, npc_data in npcs.items():
        name = npc_data.get('name', 'Unknown')
        position = str(npc_data.get('position', 'N/A'))
        dialogue = npc_data.get('dialogue_id', 'None')
        shop = npc_data.get('shop_id', 'None')
        print(f"{npc_id:<25} {name:<20} {position:<15} {dialogue:<20} {shop}")

    print(f"\nTotal NPCs: {len(npcs)}\n")


def show_location_transitions(location_name):
    """Show transitions (doors, exits, entrances) at a location"""
    # Try exact match first
    loc_id = location_name
    if loc_id not in LOCATIONS:
        # Try case-insensitive search
        matches = [lid for lid in LOCATIONS.keys() if lid.lower() == location_name.lower()]
        if matches:
            loc_id = matches[0]
        else:
            print(f"\nError: Location '{location_name}' not found.")
            return

    triggers = LOCATION_TRIGGERS.get(loc_id, {})

    print(f"\n=== Transitions at {LOCATIONS[loc_id].get('name', loc_id)} ===\n")

    if not triggers:
        print("No transitions at this location.\n")
        return

    print(f"{'Trigger ID':<25} {'Type':<15} {'Position':<15} {'Target Location'}")
    print("-" * 80)

    for trigger_id, trigger_data in triggers.items():
        trigger_type = trigger_data.get('type', 'Unknown')
        position = str(trigger_data.get('position', 'N/A'))
        target = trigger_data.get('target_location', 'N/A')
        print(f"{trigger_id:<25} {trigger_type:<15} {position:<15} {target}")

    print(f"\nTotal transitions: {len(triggers)}\n")


def show_location_encounters(location_name):
    """Show encounter data for a location"""
    # Try exact match first
    loc_id = location_name
    if loc_id not in LOCATIONS:
        # Try case-insensitive search
        matches = [lid for lid in LOCATIONS.keys() if lid.lower() == location_name.lower()]
        if matches:
            loc_id = matches[0]
        else:
            print(f"\nError: Location '{location_name}' not found.")
            return

    loc = LOCATIONS[loc_id]

    print(f"\n=== Encounters at {loc.get('name', loc_id)} ===\n")

    encounter_rate = loc.get('encounter_rate', 0.0)
    encounter_table = loc.get('encounter_table', None)

    print(f"Encounter Rate:  {encounter_rate:.2f}")
    print(f"Encounter Table: {encounter_table if encounter_table else 'None'}")

    if encounter_rate == 0.0:
        print("\nNo random encounters at this location.\n")
    else:
        print("\n(Encounter table data is referenced by ID. See data/enemies.py for enemy details.)\n")


def list_dungeons():
    """List all dungeons"""
    print("\n=== All Dungeons ===\n")
    print(f"{'ID':<30} {'Name':<35} {'Floors':<8} {'Boss'}")
    print("-" * 85)

    for dungeon_id, dungeon_data in sorted(DUNGEONS.items()):
        name = dungeon_data.get('name', 'Unknown')
        num_floors = dungeon_data.get('num_floors', 0)
        boss = dungeon_data.get('boss', 'None')
        print(f"{dungeon_id:<30} {name:<35} {num_floors:<8} {boss}")

    print(f"\nTotal dungeons: {len(DUNGEONS)}\n")


def show_dungeon_details(dungeon_name):
    """Show detailed layout for a dungeon"""
    # Try exact match first
    dungeon_id = dungeon_name
    if dungeon_id not in DUNGEONS:
        # Try case-insensitive search
        matches = [did for did in DUNGEONS.keys() if did.lower() == dungeon_name.lower()]
        if matches:
            dungeon_id = matches[0]
        else:
            print(f"\nError: Dungeon '{dungeon_name}' not found.")
            print("Use --dungeons to see all available dungeons.\n")
            return

    dungeon = DUNGEONS[dungeon_id]

    print(f"\n=== Dungeon: {dungeon.get('name', 'Unknown')} ===\n")
    print(f"ID:             {dungeon_id}")
    print(f"Floors:         {dungeon.get('num_floors', 0)}")
    print(f"Random Layout:  {'Yes' if dungeon.get('random_layout', False) else 'No'}")
    print(f"Encounter Rate: {dungeon.get('encounter_rate', 0.0):.2f}")
    print(f"Encounter Table: {dungeon.get('encounter_table', 'N/A')}")
    print(f"Boss:           {dungeon.get('boss', 'None')}")

    # Show layout if available
    layout = dungeon.get('layout', None)
    if layout and 'floors' in layout:
        print("\n--- Floor Layout ---")
        for floor_data in layout['floors']:
            floor_num = floor_data.get('floor', 0)
            rooms = floor_data.get('rooms', [])
            print(f"\nFloor {floor_num}: {len(rooms)} rooms")

            for room in rooms:
                room_id = room.get('id', 'unknown')
                room_type = room.get('type', 'unknown')
                connections = room.get('connections', [])
                print(f"  - {room_id} ({room_type}) -> {', '.join(connections)}")

    print()


def main():
    parser = argparse.ArgumentParser(
        description="Map Data Inspector - View game locations, NPCs, encounters, and dungeons",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --list
  %(prog)s --location imperial_city
  %(prog)s --npcs imperial_city
  %(prog)s --transitions imperial_city
  %(prog)s --encounters surface_forest
  %(prog)s --dungeons
  %(prog)s --dungeon tutorial_warren
        """
    )

    parser.add_argument('--list', action='store_true',
                        help='List all locations')
    parser.add_argument('--location', metavar='NAME',
                        help='Show details for a location')
    parser.add_argument('--npcs', metavar='NAME',
                        help='Show NPCs at a location')
    parser.add_argument('--transitions', metavar='NAME',
                        help='Show exits/entrances at a location')
    parser.add_argument('--encounters', metavar='NAME',
                        help='Show encounter data for a location')
    parser.add_argument('--dungeons', action='store_true',
                        help='List all dungeons')
    parser.add_argument('--dungeon', metavar='NAME',
                        help='Show details for a dungeon')

    args = parser.parse_args()

    # Handle commands
    if args.list:
        list_locations()
    elif args.location:
        show_location_details(args.location)
    elif args.npcs:
        show_location_npcs(args.npcs)
    elif args.transitions:
        show_location_transitions(args.transitions)
    elif args.encounters:
        show_location_encounters(args.encounters)
    elif args.dungeons:
        list_dungeons()
    elif args.dungeon:
        show_dungeon_details(args.dungeon)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
