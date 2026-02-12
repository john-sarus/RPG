"""
Stat Viewer CLI Tool
View character stats, growth curves, and compare characters
"""

import os
import sys
import argparse

# Set headless mode BEFORE any pygame import
os.environ['SDL_VIDEODRIVER'] = 'dummy'

# Setup sys.path to import game modules
script_dir = os.path.dirname(os.path.abspath(__file__))
shim_dir = os.path.join(script_dir, '..', 'shim')
project_root = os.path.join(script_dir, '..', '..')

sys.path.insert(0, shim_dir)
sys.path.insert(1, project_root)

# Import game modules
from data.characters import CHARACTERS, get_character_stats_at_level
from utils.level_up_system import calculate_exp_for_level, get_exp_to_next_level


def display_character_stats(char_id, level=1):
    """Display stats for a single character at a given level"""
    if char_id not in CHARACTERS:
        print(f"Error: Character '{char_id}' not found.")
        print(f"Valid characters: {', '.join(sorted(CHARACTERS.keys()))}")
        return

    char = CHARACTERS[char_id]
    stats = get_character_stats_at_level(char_id, level)

    print(f"\n{'=' * 60}")
    print(f"Character: {char['name']} ({char_id})")
    print(f"Class: {char['starting_class']}")
    if char['evolved_class']:
        print(f"Evolved Class: {char['evolved_class']}")
    print(f"Level: {level}")
    print(f"{'=' * 60}")

    # Stat table
    print(f"\n{'Stat':<20} {'Base':<10} {f'At Level {level}':<15}")
    print(f"{'-' * 60}")

    stat_names = {
        'hp': 'HP',
        'mp': 'MP',
        'attack': 'Attack',
        'defense': 'Defense',
        'magic_power': 'Magic Power',
        'spell_resistance': 'Spell Resistance',
        'speed': 'Speed'
    }

    for stat_key, stat_display in stat_names.items():
        base_value = char['base_stats'][stat_key]
        level_value = int(stats[stat_key])
        growth_rate = char['growth_rates'][stat_key]
        print(f"{stat_display:<20} {base_value:<10} {level_value:<15} (+{growth_rate}/level)")

    # Experience info
    if level < 99:
        exp_for_current = calculate_exp_for_level(level)
        exp_for_next = calculate_exp_for_level(level + 1)
        exp_needed = exp_for_next - exp_for_current
        print(f"\n{'Experience':<20} {f'Total for Lv{level}':<20} {'To Next Level':<20}")
        print(f"{'-' * 60}")
        print(f"{'':20} {exp_for_current:<20} {exp_needed:<20}")
    else:
        print(f"\nMax level reached!")

    print()


def compare_characters(char_id1, char_id2, level=1):
    """Compare stats for two characters side by side"""
    if char_id1 not in CHARACTERS:
        print(f"Error: Character '{char_id1}' not found.")
        return
    if char_id2 not in CHARACTERS:
        print(f"Error: Character '{char_id2}' not found.")
        return

    char1 = CHARACTERS[char_id1]
    char2 = CHARACTERS[char_id2]
    stats1 = get_character_stats_at_level(char_id1, level)
    stats2 = get_character_stats_at_level(char_id2, level)

    print(f"\n{'=' * 80}")
    print(f"Character Comparison at Level {level}")
    print(f"{'=' * 80}")
    print(f"{'':<20} {char1['name'] + ' (' + char_id1 + ')':<30} {char2['name'] + ' (' + char_id2 + ')':<30}")
    print(f"{'-' * 80}")

    stat_names = {
        'hp': 'HP',
        'mp': 'MP',
        'attack': 'Attack',
        'defense': 'Defense',
        'magic_power': 'Magic Power',
        'spell_resistance': 'Spell Resistance',
        'speed': 'Speed'
    }

    for stat_key, stat_display in stat_names.items():
        val1 = int(stats1[stat_key])
        val2 = int(stats2[stat_key])

        # Highlight which is higher
        if val1 > val2:
            marker1, marker2 = ' ★', '  '
        elif val2 > val1:
            marker1, marker2 = '  ', ' ★'
        else:
            marker1, marker2 = '  ', '  '

        print(f"{stat_display:<20} {val1:>5}{marker1:<25} {val2:>5}{marker2:<25}")

    print()


def display_all_characters(level=1):
    """Display summary table for all characters"""
    print(f"\n{'=' * 100}")
    print(f"All Characters at Level {level}")
    print(f"{'=' * 100}")
    print(f"{'Name':<15} {'ID':<15} {'Class':<20} {'HP':>6} {'Attack':>8} {'Speed':>7}")
    print(f"{'-' * 100}")

    for char_id in sorted(CHARACTERS.keys()):
        char = CHARACTERS[char_id]
        stats = get_character_stats_at_level(char_id, level)

        hp = int(stats['hp'])
        attack = int(stats['attack'])
        speed = int(stats['speed'])

        print(f"{char['name']:<15} {char_id:<15} {char['starting_class']:<20} {hp:>6} {attack:>8} {speed:>7}")

    print()


def main():
    parser = argparse.ArgumentParser(
        description='View and compare character stats and growth curves',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python stat_viewer.py --character javin --level 50
  python stat_viewer.py --compare javin,fei --level 25
  python stat_viewer.py --all --level 1
  python stat_viewer.py --all --level 99
        """
    )

    parser.add_argument('--character', type=str,
                        help='Character ID (lowercase) to view stats for')
    parser.add_argument('--level', type=int, default=1,
                        help='Level to calculate stats at (1-99, default: 1)')
    parser.add_argument('--compare', type=str,
                        help='Compare two characters: NAME1,NAME2 (comma-separated lowercase IDs)')
    parser.add_argument('--all', action='store_true',
                        help='Show summary table for all characters')

    args = parser.parse_args()

    # Validate level
    if args.level < 1 or args.level > 99:
        print("Error: Level must be between 1 and 99.")
        return

    # Handle different modes
    if args.all:
        display_all_characters(args.level)
    elif args.compare:
        parts = args.compare.split(',')
        if len(parts) != 2:
            print("Error: --compare requires exactly two character IDs separated by a comma.")
            print("Example: --compare javin,fei")
            return
        char_id1, char_id2 = parts[0].strip(), parts[1].strip()
        compare_characters(char_id1, char_id2, args.level)
    elif args.character:
        display_character_stats(args.character, args.level)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
