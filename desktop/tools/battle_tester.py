"""
Battle Tester CLI - Development tool for testing combat scenarios

Usage:
    python desktop/tools/battle_tester.py --party javin,fei --level 10 --enemies infected_kobold_weak,skeleton --rounds 1 --verbose

This tool runs auto-battles (no interactive input) and reports results.
"""

import os
import sys
import argparse
import random

# Set headless mode BEFORE any pygame/game imports
os.environ['SDL_VIDEODRIVER'] = 'dummy'

# Set up sys.path to find shim and game modules
script_dir = os.path.dirname(os.path.abspath(__file__))
shim_dir = os.path.join(script_dir, '..', 'shim')
project_root = os.path.join(script_dir, '..', '..')

sys.path.insert(0, os.path.abspath(shim_dir))
sys.path.insert(1, os.path.abspath(project_root))

# Now safe to import game modules
from utils.game_state import GameState
from utils.battle_engine import BattleEngine
from utils.level_up_system import add_experience, calculate_exp_for_level
from data.characters import CHARACTERS
from data.enemies import ENEMIES


def setup_party(party_ids, target_level, verbose=False):
    """
    Set up party with characters at specified level

    Args:
        party_ids: List of character IDs (lowercase)
        target_level: Target level for all characters
        verbose: Print verbose output

    Returns:
        GameState with configured party
    """
    game_state = GameState()

    # Clear default party
    game_state.active_party = []

    # Add each character to party
    for char_id in party_ids:
        if char_id not in CHARACTERS:
            print(f"ERROR: Unknown character '{char_id}'. Valid characters: {', '.join(CHARACTERS.keys())}")
            sys.exit(1)

        # Add to active party
        game_state.active_party.append(char_id)

        # Level up to target level
        if target_level > 1:
            # Calculate EXP needed for target level
            exp_needed = calculate_exp_for_level(target_level)
            result = add_experience(game_state, char_id, exp_needed)

            if verbose and result:
                print(f"  {CHARACTERS[char_id]['name']} leveled to {result.get('new_level', target_level)}")

    if verbose:
        print(f"\nParty setup complete:")
        for char_id in game_state.active_party:
            char = game_state.characters[char_id]
            print(f"  - {CHARACTERS[char_id]['name']}: Lv{char['level']} HP:{char['hp']}/{char['max_hp']} ATK:{char['stats']['attack']} SPD:{char['stats']['speed']}")
        print()

    return game_state


def run_auto_battle(game_state, enemy_ids, verbose=False):
    """
    Run an auto-battle simulation

    Args:
        game_state: GameState instance
        enemy_ids: List of enemy IDs
        verbose: Print verbose turn-by-turn output

    Returns:
        dict: Battle results
    """
    # Validate enemy IDs
    for enemy_id in enemy_ids:
        if enemy_id not in ENEMIES:
            print(f"ERROR: Unknown enemy '{enemy_id}'. Valid enemies: {', '.join(list(ENEMIES.keys())[:10])}...")
            sys.exit(1)

    # Create battle engine
    battle = BattleEngine(game_state, enemy_ids, can_flee=True)

    if verbose:
        print(f"Battle Start! Party vs {len(battle.enemies)} enemies")
        print(f"Turn order (by speed): {[a['id'] for a in battle.turn_order]}\n")

    turn_count = 0
    max_turns = 100  # Prevent infinite loops

    while not battle.battle_over and turn_count < max_turns:
        turn_count += 1

        actor = battle.get_current_actor()
        if not actor:
            break

        actor_name = CHARACTERS[actor['id']]['name'] if actor['type'] == 'player' else ENEMIES[actor['id']]['name']

        if actor['type'] == 'player':
            # Player turn - pick random attack on random alive enemy
            alive_enemies = [e for e in battle.enemies if e['hp'] > 0]
            if alive_enemies:
                target = random.choice(alive_enemies)
                target_name = ENEMIES[target['id']]['name']

                # Execute attack
                damage = battle.calculate_physical_damage(actor, target)
                target['hp'] -= damage

                if verbose:
                    print(f"Turn {turn_count}: {actor_name} attacks {target_name} for {damage} damage! (HP: {max(0, target['hp'])}/{target['max_hp']})")

        else:
            # Enemy turn - use AI
            action = battle.ai_select_action(actor)

            if action and action.get('target'):
                target = action['target']

                if action['action'] == 'attack':
                    # Physical attack
                    target_name = CHARACTERS[target['id']]['name'] if target['type'] == 'player' else ENEMIES[target['id']]['name']
                    damage = battle.calculate_physical_damage(actor, target)

                    if target['type'] == 'player':
                        target['data']['hp'] -= damage
                        if verbose:
                            print(f"Turn {turn_count}: {actor_name} attacks {target_name} for {damage} damage! (HP: {max(0, target['data']['hp'])}/{target['data']['max_hp']})")
                    else:
                        target['hp'] -= damage
                        if verbose:
                            print(f"Turn {turn_count}: {actor_name} attacks {target_name} for {damage} damage! (HP: {max(0, target['hp'])}/{target['max_hp']})")

        # Next turn
        battle.next_turn()
        battle.check_battle_end()

    # Gather results
    results = {
        'victory': battle.victory,
        'turns': turn_count,
        'party_survivors': [],
        'rewards': battle.get_battle_rewards() if battle.victory else {'exp': 0, 'gil': 0}
    }

    # Count survivors
    for member in battle.party:
        if member['data']['hp'] > 0:
            results['party_survivors'].append({
                'id': member['id'],
                'name': CHARACTERS[member['id']]['name'],
                'hp': member['data']['hp'],
                'max_hp': member['data']['max_hp']
            })

    return results


def main():
    parser = argparse.ArgumentParser(
        description='Battle Tester CLI - Automated combat simulation tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single character vs weak enemy
  python desktop/tools/battle_tester.py --party javin --level 1 --enemies infected_kobold_weak

  # Full party at level 10 vs multiple enemies
  python desktop/tools/battle_tester.py --party javin,fei,iris --level 10 --enemies skeleton,skeleton --verbose

  # Run 5 rounds of battles
  python desktop/tools/battle_tester.py --party javin --level 5 --enemies infected_kobold_weak --rounds 5
        """
    )

    parser.add_argument(
        '--party',
        type=str,
        default='javin',
        help='Comma-separated character IDs (lowercase). Example: javin,fei,iris'
    )

    parser.add_argument(
        '--level',
        type=int,
        default=1,
        help='Level for all party members (1-99). Default: 1'
    )

    parser.add_argument(
        '--enemies',
        type=str,
        default='infected_kobold_weak',
        help='Comma-separated enemy IDs (snake_case). Example: infected_kobold_weak,skeleton'
    )

    parser.add_argument(
        '--rounds',
        type=int,
        default=1,
        help='Number of battle rounds to run. Default: 1'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Print turn-by-turn battle details'
    )

    args = parser.parse_args()

    # Parse party and enemy IDs
    party_ids = [cid.strip() for cid in args.party.split(',')]
    enemy_ids = [eid.strip() for eid in args.enemies.split(',')]

    # Validate level
    if args.level < 1 or args.level > 99:
        print("ERROR: Level must be between 1 and 99")
        sys.exit(1)

    print("=" * 60)
    print("BATTLE TESTER CLI")
    print("=" * 60)
    print(f"Party: {', '.join([CHARACTERS[cid]['name'] for cid in party_ids])}")
    print(f"Level: {args.level}")
    print(f"Enemies: {', '.join([ENEMIES[eid]['name'] for eid in enemy_ids])}")
    print(f"Rounds: {args.rounds}")
    print("=" * 60)
    print()

    # Run battles
    victories = 0
    defeats = 0
    total_turns = 0
    total_exp = 0
    total_gil = 0

    for round_num in range(1, args.rounds + 1):
        if args.rounds > 1:
            print(f"\n--- Round {round_num} ---\n")

        # Set up fresh party for each round
        game_state = setup_party(party_ids, args.level, verbose=args.verbose)

        # Run battle
        results = run_auto_battle(game_state, enemy_ids, verbose=args.verbose)

        # Track results
        if results['victory']:
            victories += 1
            total_exp += results['rewards']['exp']
            total_gil += results['rewards']['gil']
        else:
            defeats += 1

        total_turns += results['turns']

        # Print round summary
        if results['victory']:
            print(f"\n✓ VICTORY in {results['turns']} turns!")
            print(f"  Rewards: {results['rewards']['exp']} EXP, {results['rewards']['gil']} Gil")
            print(f"  Survivors: {len(results['party_survivors'])}/{len(party_ids)}")
            for survivor in results['party_survivors']:
                print(f"    - {survivor['name']}: {survivor['hp']}/{survivor['max_hp']} HP")
        else:
            print(f"\n✗ DEFEAT after {results['turns']} turns")

    # Print overall summary
    if args.rounds > 1:
        print("\n" + "=" * 60)
        print("OVERALL RESULTS")
        print("=" * 60)
        print(f"Victories: {victories}/{args.rounds} ({100*victories//args.rounds}%)")
        print(f"Defeats: {defeats}/{args.rounds}")
        print(f"Average turns per battle: {total_turns/args.rounds:.1f}")
        if victories > 0:
            print(f"Total rewards: {total_exp} EXP, {total_gil} Gil")
            print(f"Average per victory: {total_exp//victories} EXP, {total_gil//victories} Gil")
        print("=" * 60)


if __name__ == '__main__':
    main()
