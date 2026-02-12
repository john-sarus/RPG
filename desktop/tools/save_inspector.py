"""
Save Inspector CLI Tool

View, diff, and edit JSON save files for There Will Be Kobolds.
Provides read-only inspection and safe editing with automatic backups.
"""

import os
import sys
import json
import argparse
import shutil
from datetime import datetime

# Set up headless mode before any imports
os.environ['SDL_VIDEODRIVER'] = 'dummy'

# Set up sys.path to import game modules
script_dir = os.path.dirname(os.path.abspath(__file__))
shim_dir = os.path.join(script_dir, '..', 'shim')
project_root = os.path.join(script_dir, '..', '..')

sys.path.insert(0, os.path.abspath(shim_dir))
sys.path.insert(1, os.path.abspath(project_root))

# Import game modules
from utils.save_system import SaveSystem
from utils.game_state import GameState
from data.characters import CHARACTERS


def format_time(seconds):
    """Format playtime in seconds to readable string"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours}h {minutes}m {secs}s"


def list_saves(save_dir='saves'):
    """List all save files with summary info"""
    ss = SaveSystem(save_directory=save_dir)
    saves = ss.list_saves()

    if not saves:
        print("No save files found.")
        return

    print(f"\n{'Slot':<6} {'Timestamp':<25} {'Location':<20} {'Party':<8} {'Gil':<10} {'Playtime':<15}")
    print("=" * 100)

    for save_info in saves:
        timestamp = save_info['timestamp'][:19] if save_info.get('timestamp') else 'Unknown'
        location = save_info.get('location', 'Unknown')[:19]
        party_size = save_info.get('party_size', 0)
        gil = save_info.get('gil', 0)
        playtime = format_time(save_info.get('playtime', 0))

        print(f"{save_info['slot']:<6} {timestamp:<25} {location:<20} {party_size:<8} {gil:<10} {playtime:<15}")

    # Check for special saves
    autosave_path = os.path.join(save_dir, 'autosave.json')
    quicksave_path = os.path.join(save_dir, 'quicksave.json')

    if os.path.exists(autosave_path):
        print("\n[Autosave exists]")
    if os.path.exists(quicksave_path):
        print("[Quicksave exists]")


def view_save(slot, save_dir='saves'):
    """View detailed save file contents"""
    ss = SaveSystem(save_directory=save_dir)

    # Determine save type
    if slot == 'autosave':
        save_data = ss.load_game(save_type='auto')
        title = "AUTOSAVE"
    elif slot == 'quicksave':
        save_data = ss.load_game(save_type='quick')
        title = "QUICKSAVE"
    else:
        try:
            slot_num = int(slot)
            save_data = ss.load_game(slot=slot_num, save_type='manual')
            title = f"SAVE SLOT {slot_num}"
        except ValueError:
            print(f"Error: Invalid slot '{slot}'. Use a number, 'autosave', or 'quicksave'.")
            return

    if not save_data:
        print(f"No save data found for slot: {slot}")
        return

    print(f"\n{'=' * 80}")
    print(f"{title.center(80)}")
    print(f"{'=' * 80}\n")

    # Basic Info
    print(f"Timestamp: {save_data.get('timestamp', 'Unknown')}")
    print(f"Version: {save_data.get('version', 'Unknown')}")
    print(f"Playtime: {format_time(save_data.get('playtime_seconds', 0))}")
    print(f"Location: {save_data.get('current_location', 'Unknown')}")
    print(f"New Game+: {save_data.get('new_game_plus', False)}")
    print(f"Playthrough: {save_data.get('playthrough_count', 1)}")

    # Party
    print(f"\n{'PARTY'.center(80, '-')}")
    party = save_data.get('party', {})
    active = party.get('active', [])
    reserves = party.get('reserves', [])
    characters = party.get('characters', {})

    print(f"\nActive Party: {', '.join(active) if active else 'None'}")
    print(f"Reserves: {', '.join(reserves) if reserves else 'None'}")

    if characters:
        print(f"\n{'Name':<15} {'Level':<8} {'HP':<12} {'MP':<12} {'Attack':<10} {'Defense':<10}")
        print("-" * 80)
        for char_id in active + reserves:
            if char_id in characters:
                char = characters[char_id]
                stats = char.get('stats', {})
                print(f"{char_id:<15} {char.get('level', 1):<8} "
                      f"{stats.get('hp', 0)}/{stats.get('max_hp', 0):<12} "
                      f"{stats.get('mp', 0)}/{stats.get('max_mp', 0):<12} "
                      f"{stats.get('attack', 0):<10} {stats.get('defense', 0):<10}")

    # Inventory
    print(f"\n{'INVENTORY'.center(80, '-')}")
    inventory = save_data.get('inventory', {})
    items = inventory.get('items', {})
    equipment = inventory.get('equipment', {})
    key_items = inventory.get('key_items', [])
    gil = inventory.get('gil', 0)

    print(f"\nGil: {gil}")

    if items:
        print(f"\nItems:")
        for item_id, count in items.items():
            print(f"  {item_id}: {count}")

    if equipment:
        print(f"\nEquipment:")
        for equip_id, count in equipment.items():
            print(f"  {equip_id}: {count}")

    if key_items:
        print(f"\nKey Items:")
        for key_item in key_items:
            print(f"  - {key_item}")

    # Story Flags
    print(f"\n{'STORY FLAGS'.center(80, '-')}")
    flags = save_data.get('story_flags', {})

    # Group flags by category
    categories = {
        'Tutorial': ['tutorial_complete', 'baby_dragon_saved'],
        'Warren': ['warren_infected', 'kella_went_to_wake_dragons'],
        'Surface': ['met_frostbite', 'met_fei'],
        'Imperial City': ['imperial_city_visited', 'met_michael', 'met_flood', 'met_hannah'],
        'Recruitment': ['met_orisia', 'recruitment_deadline_passed', 'fritzzit_crankpot_available'],
        'Major Events': ['first_dragon_defeated', 'second_dragon_defeated', 'flood_dead', 'cure_found'],
        'Yipp': ['yipp_encountered', 'yipp_alignment', 'yipp_betrayed'],
        'Endings': ['necromancer_defeated', 'ending_achieved'],
        'Post-Game': ['post_credits_unlocked', 'slaver_island_completed', 'secret_boss_defeated']
    }

    for category, flag_keys in categories.items():
        relevant_flags = {k: flags.get(k) for k in flag_keys if k in flags and flags.get(k)}
        if relevant_flags:
            print(f"\n{category}:")
            for flag_key, flag_value in relevant_flags.items():
                if isinstance(flag_value, bool):
                    print(f"  {flag_key}: {'✓' if flag_value else '✗'}")
                else:
                    print(f"  {flag_key}: {flag_value}")

    # Character Recruitment
    print(f"\n{'RECRUITED CHARACTERS'.center(80, '-')}")
    recruited = save_data.get('characters_recruited', [])
    lost = save_data.get('lost_characters', [])

    if recruited:
        print(f"Recruited: {', '.join(recruited)}")
    if lost:
        print(f"Lost: {', '.join(lost)}")


def diff_saves(slot1, slot2, save_dir='saves'):
    """Compare two save files and show differences"""
    ss = SaveSystem(save_directory=save_dir)

    # Load both saves
    try:
        if slot1 == 'autosave':
            data1 = ss.load_game(save_type='auto')
            label1 = "Autosave"
        elif slot1 == 'quicksave':
            data1 = ss.load_game(save_type='quick')
            label1 = "Quicksave"
        else:
            data1 = ss.load_game(slot=int(slot1), save_type='manual')
            label1 = f"Slot {slot1}"

        if slot2 == 'autosave':
            data2 = ss.load_game(save_type='auto')
            label2 = "Autosave"
        elif slot2 == 'quicksave':
            data2 = ss.load_game(save_type='quick')
            label2 = "Quicksave"
        else:
            data2 = ss.load_game(slot=int(slot2), save_type='manual')
            label2 = f"Slot {slot2}"
    except (ValueError, TypeError) as e:
        print(f"Error: Invalid slot specification: {e}")
        return

    if not data1:
        print(f"Error: Could not load {label1}")
        return
    if not data2:
        print(f"Error: Could not load {label2}")
        return

    print(f"\n{'=' * 80}")
    print(f"DIFF: {label1} → {label2}".center(80))
    print(f"{'=' * 80}\n")

    differences = []

    # Compare key fields
    if data1.get('current_location') != data2.get('current_location'):
        differences.append(f"Location: {data1.get('current_location')} → {data2.get('current_location')}")

    if data1.get('inventory', {}).get('gil') != data2.get('inventory', {}).get('gil'):
        gil1 = data1.get('inventory', {}).get('gil', 0)
        gil2 = data2.get('inventory', {}).get('gil', 0)
        diff = gil2 - gil1
        differences.append(f"Gil: {gil1} → {gil2} ({'+' if diff >= 0 else ''}{diff})")

    # Compare party
    party1 = set(data1.get('party', {}).get('active', []))
    party2 = set(data2.get('party', {}).get('active', []))

    added = party2 - party1
    removed = party1 - party2

    if added:
        differences.append(f"Party Added: {', '.join(added)}")
    if removed:
        differences.append(f"Party Removed: {', '.join(removed)}")

    # Compare story flags
    flags1 = data1.get('story_flags', {})
    flags2 = data2.get('story_flags', {})

    flag_changes = []
    for flag_key in set(list(flags1.keys()) + list(flags2.keys())):
        val1 = flags1.get(flag_key)
        val2 = flags2.get(flag_key)
        if val1 != val2:
            flag_changes.append(f"  {flag_key}: {val1} → {val2}")

    if flag_changes:
        differences.append("Story Flags Changed:")
        differences.extend(flag_changes)

    # Compare items
    items1 = data1.get('inventory', {}).get('items', {})
    items2 = data2.get('inventory', {}).get('items', {})

    item_changes = []
    for item_id in set(list(items1.keys()) + list(items2.keys())):
        count1 = items1.get(item_id, 0)
        count2 = items2.get(item_id, 0)
        if count1 != count2:
            item_changes.append(f"  {item_id}: {count1} → {count2}")

    if item_changes:
        differences.append("Items Changed:")
        differences.extend(item_changes)

    # Print results
    if not differences:
        print("No differences found.")
    else:
        for diff in differences:
            print(diff)


def set_flag(slot, flag_key, value, save_dir='saves'):
    """Set a story flag in a save file (with backup)"""
    ss = SaveSystem(save_directory=save_dir)

    # Determine filename
    if slot == 'autosave':
        filename = os.path.join(save_dir, 'autosave.json')
    elif slot == 'quicksave':
        filename = os.path.join(save_dir, 'quicksave.json')
    else:
        try:
            slot_num = int(slot)
            filename = os.path.join(save_dir, f'save_{slot_num:03d}.json')
        except ValueError:
            print(f"Error: Invalid slot '{slot}'")
            return

    if not os.path.exists(filename):
        print(f"Error: Save file does not exist: {filename}")
        return

    # Create backup
    backup_filename = f"{filename}.bak"
    shutil.copy2(filename, backup_filename)
    print(f"Backup created: {backup_filename}")

    # Load save data
    try:
        with open(filename, 'r') as f:
            save_data = json.load(f)
    except Exception as e:
        print(f"Error loading save file: {e}")
        return

    # Parse value
    if value.lower() in ('true', 'yes', '1'):
        parsed_value = True
    elif value.lower() in ('false', 'no', '0'):
        parsed_value = False
    elif value.lower() == 'none':
        parsed_value = None
    else:
        # Try to parse as string
        parsed_value = value

    # Set flag
    if 'story_flags' not in save_data:
        save_data['story_flags'] = {}

    old_value = save_data['story_flags'].get(flag_key)
    save_data['story_flags'][flag_key] = parsed_value

    # Write modified save
    try:
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)
        print(f"\nFlag updated successfully:")
        print(f"  {flag_key}: {old_value} → {parsed_value}")
    except Exception as e:
        print(f"Error writing save file: {e}")
        # Restore backup
        shutil.copy2(backup_filename, filename)
        print("Backup restored.")


def add_item(slot, item_id, count, save_dir='saves'):
    """Add items to inventory in a save file (with backup)"""
    ss = SaveSystem(save_directory=save_dir)

    # Determine filename
    if slot == 'autosave':
        filename = os.path.join(save_dir, 'autosave.json')
    elif slot == 'quicksave':
        filename = os.path.join(save_dir, 'quicksave.json')
    else:
        try:
            slot_num = int(slot)
            filename = os.path.join(save_dir, f'save_{slot_num:03d}.json')
        except ValueError:
            print(f"Error: Invalid slot '{slot}'")
            return

    if not os.path.exists(filename):
        print(f"Error: Save file does not exist: {filename}")
        return

    # Create backup
    backup_filename = f"{filename}.bak"
    shutil.copy2(filename, backup_filename)
    print(f"Backup created: {backup_filename}")

    # Load save data
    try:
        with open(filename, 'r') as f:
            save_data = json.load(f)
    except Exception as e:
        print(f"Error loading save file: {e}")
        return

    # Parse count
    try:
        count_int = int(count)
    except ValueError:
        print(f"Error: Invalid count '{count}'. Must be an integer.")
        return

    # Add item
    if 'inventory' not in save_data:
        save_data['inventory'] = {}
    if 'items' not in save_data['inventory']:
        save_data['inventory']['items'] = {}

    old_count = save_data['inventory']['items'].get(item_id, 0)
    new_count = old_count + count_int

    if new_count <= 0:
        # Remove item if count reaches zero or below
        if item_id in save_data['inventory']['items']:
            del save_data['inventory']['items'][item_id]
        new_count = 0
    else:
        save_data['inventory']['items'][item_id] = new_count

    # Write modified save
    try:
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)
        print(f"\nInventory updated successfully:")
        print(f"  {item_id}: {old_count} → {new_count}")
    except Exception as e:
        print(f"Error writing save file: {e}")
        # Restore backup
        shutil.copy2(backup_filename, filename)
        print("Backup restored.")


def set_level(slot, char_id, level, save_dir='saves'):
    """Set character level in a save file (with backup and stat recalculation)"""
    ss = SaveSystem(save_directory=save_dir)

    # Validate character ID
    if char_id not in CHARACTERS:
        print(f"Error: Unknown character '{char_id}'")
        print(f"Valid characters: {', '.join(CHARACTERS.keys())}")
        return

    # Determine filename
    if slot == 'autosave':
        filename = os.path.join(save_dir, 'autosave.json')
    elif slot == 'quicksave':
        filename = os.path.join(save_dir, 'quicksave.json')
    else:
        try:
            slot_num = int(slot)
            filename = os.path.join(save_dir, f'save_{slot_num:03d}.json')
        except ValueError:
            print(f"Error: Invalid slot '{slot}'")
            return

    if not os.path.exists(filename):
        print(f"Error: Save file does not exist: {filename}")
        return

    # Parse level
    try:
        level_int = int(level)
        if level_int < 1 or level_int > 99:
            print("Error: Level must be between 1 and 99")
            return
    except ValueError:
        print(f"Error: Invalid level '{level}'. Must be an integer.")
        return

    # Create backup
    backup_filename = f"{filename}.bak"
    shutil.copy2(filename, backup_filename)
    print(f"Backup created: {backup_filename}")

    # Load save data
    try:
        with open(filename, 'r') as f:
            save_data = json.load(f)
    except Exception as e:
        print(f"Error loading save file: {e}")
        return

    # Ensure character exists in save
    if 'party' not in save_data:
        save_data['party'] = {}
    if 'characters' not in save_data['party']:
        save_data['party']['characters'] = {}

    if char_id not in save_data['party']['characters']:
        print(f"Warning: Character '{char_id}' not found in save. Creating entry...")
        save_data['party']['characters'][char_id] = {
            'level': 1,
            'stats': {}
        }

    # Get character data
    char_data = CHARACTERS[char_id]
    base_stats = char_data['base_stats']
    growth_rates = char_data['growth_rates']

    # Recalculate stats for new level
    new_stats = {}
    for stat_key in ['hp', 'mp', 'attack', 'defense', 'magic_power', 'spell_resistance', 'speed']:
        base = base_stats.get(stat_key, 0)
        growth = growth_rates.get(stat_key, 0)
        new_stats[stat_key] = int(base + growth * (level_int - 1))

    # Set max HP/MP as well
    new_stats['max_hp'] = new_stats['hp']
    new_stats['max_mp'] = new_stats['mp']

    # Update character
    old_level = save_data['party']['characters'][char_id].get('level', 1)
    save_data['party']['characters'][char_id]['level'] = level_int
    save_data['party']['characters'][char_id]['stats'] = new_stats

    # Write modified save
    try:
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)
        print(f"\nCharacter updated successfully:")
        print(f"  {char_id}: Level {old_level} → {level_int}")
        print(f"  Stats recalculated: HP={new_stats['hp']}, Attack={new_stats['attack']}, Defense={new_stats['defense']}")
    except Exception as e:
        print(f"Error writing save file: {e}")
        # Restore backup
        shutil.copy2(backup_filename, filename)
        print("Backup restored.")


def main():
    parser = argparse.ArgumentParser(
        description='Save Inspector - View, diff, and edit save files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --list
  %(prog)s --view 1
  %(prog)s --view autosave
  %(prog)s --diff 1 2
  %(prog)s --set-flag 1 met_orisia true
  %(prog)s --add-item 1 potion 10
  %(prog)s --set-level 1 javin 50
        """
    )

    parser.add_argument('--list', action='store_true',
                        help='List all save files with summary')
    parser.add_argument('--view', metavar='SLOT',
                        help='View detailed save contents (slot number, autosave, or quicksave)')
    parser.add_argument('--diff', nargs=2, metavar=('SLOT1', 'SLOT2'),
                        help='Compare two save files')
    parser.add_argument('--set-flag', nargs=3, metavar=('SLOT', 'FLAG', 'VALUE'),
                        help='Set a story flag (creates backup)')
    parser.add_argument('--add-item', nargs=3, metavar=('SLOT', 'ITEM', 'COUNT'),
                        help='Add items to inventory (creates backup)')
    parser.add_argument('--set-level', nargs=3, metavar=('SLOT', 'CHAR', 'LEVEL'),
                        help='Set character level (creates backup, recalculates stats)')
    parser.add_argument('--save-dir', default='saves',
                        help='Save directory path (default: saves)')

    args = parser.parse_args()

    # Execute command
    if args.list:
        list_saves(args.save_dir)
    elif args.view:
        view_save(args.view, args.save_dir)
    elif args.diff:
        diff_saves(args.diff[0], args.diff[1], args.save_dir)
    elif args.set_flag:
        set_flag(args.set_flag[0], args.set_flag[1], args.set_flag[2], args.save_dir)
    elif args.add_item:
        add_item(args.add_item[0], args.add_item[1], args.add_item[2], args.save_dir)
    elif args.set_level:
        set_level(args.set_level[0], args.set_level[1], args.set_level[2], args.save_dir)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
