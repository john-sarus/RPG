# There Will Be Kobolds -- Quickstart Guide

A dark fantasy JRPG for desktop, inspired by Final Fantasy 4-6.

---

## Get the Code

Clone the repository from GitHub:

```bash
git clone https://github.com/JT-Savage/RPG.git
cd RPG
```

The default branch is `claude/jrpg-mobile-game-KtwFT`. That branch contains the latest stable code.

---

## Launch the Game

You need Python 3.8+ and pip.

```bash
pip install -r desktop/requirements.txt
python desktop/run.py
```

A 1024x896 window opens with the title screen. If you see `ImportError: No module named 'pygame'`, run `pip install pygame-ce` and try again.

---

## Controls

### Keyboard

| Key | Action |
|-----|--------|
| Arrow Keys / WASD | Move, navigate menus |
| Enter / Space | Confirm, interact with NPCs |
| Escape | Cancel, go back, open menu |
| M | Open party menu (while exploring) |
| 1-9 | Quick-select menu items |

### Mouse

| Input | Action |
|-------|--------|
| Left click | Select, interact |
| Right click | Cancel, go back |

---

## Starting a New Game

The title screen offers four options: **New Game**, **Continue** (loads autosave), **Load Game** (pick from 100 save slots), and **Exit**.

Choose New Game. You begin as **Javin**, a Claw Noble, escaping a kobold warren overrun by undead infection. The tutorial teaches movement, combat, and interaction. After escaping, you explore the world, recruit allies, and pursue a cure for the infection.

---

## Combat

Battles are turn-based. Turn order depends on each character's Speed stat.

On your turn, pick one action:

- **Attack** -- Physical strike. Damage = your Attack minus enemy Defense.
- **Magic** -- Cast a spell. Costs MP equal to the spell's level (a level-3 spell costs 3 MP).
- **Items** -- Use a consumable from inventory (potions, antidotes, grenades).
- **Defend** -- Reduce incoming damage until your next turn.
- **Switch** -- Swap an active party member for one in reserve.
- **Flee** -- Attempt to escape. Fails against bosses.

After winning, you earn EXP (levels your characters), Gil (currency for shops), and sometimes item drops.

---

## Party System

You field 3 active characters in battle. The remaining recruits sit in reserve. Switch between active and reserve members at any time through the menu or mid-combat.

### The 12 Characters

**Required (join through the story):**

| Character | Class | Role |
|-----------|-------|------|
| Javin | Claw Noble | Fast melee, psychic damage |
| Frostbite | Gunner | High physical damage, grenades |
| Fei | Warrior | Tank with shield, highest HP |
| Michael | Cleric | Healer, holy magic |
| Flood | Ice Mage | Strongest magic user |
| Hannah | Witch | Multi-element offense (fire, thunder, earth, wind) |
| Warghoul | Undead Warrior | Dark magic, skeleton summoning |

**Optional (recruit before the deadline):**

| Character | Class | Where to Find |
|-----------|-------|---------------|
| Cookie | Druid | Halfling Rescue event |
| Iris | Nature Druid | Halfling Rescue event |
| Fritzzit | Sniper | Imperial City Inn |
| Crankpot | Firemage | Imperial City Inn |
| Yipp | Necromancer | Random dungeons, pre-Orisia only |

---

## Leveling Up

Characters gain levels from EXP. Max level starts at 75 and increases to 99 after class evolution.

Every 10 levels, a character unlocks a new combat ability. Examples:

- Fei, level 10: Power Strike (heavy single-target hit)
- Flood, level 40: Double Cast (spend 2x MP for doubled spell power)
- Fritzzit, level 90: Deadeye (critical hits deal 3x damage instead of 2x)

### Class Evolution

Most characters can evolve into an advanced class (Warrior becomes Weapon Master, Cleric becomes Paladin, etc.). Evolution requires finding a specific **key item** in a dungeon and completing a sidequest through Orisia. Evolution raises the level cap to 99 and grants new abilities.

---

## Magic

Spells cost MP equal to their level. A level-1 spell (Fire, Cure) costs 1 MP. A level-9 spell (Diamond Dust) costs 9 MP.

Only certain characters learn magic, and each is restricted to specific elements:

| Character | Elements |
|-----------|----------|
| Michael | Holy, Healing |
| Flood | Ice, Water |
| Hannah | Fire, Thunder, Earth, Wind |
| Warghoul | Dark, Necromancy |
| Cookie | Nature, Control |
| Crankpot | Fire |
| Yipp | Necromancy, Dark (or Holy if evolved to Saint) |

Buy new spells at magic shops in Imperial City and the Desert Outpost.

---

## Equipment and Items

### Equipment

Each character equips a weapon, armor, and accessory. Weapon and armor types are class-restricted -- Fei wields swords, axes, and spears; mages use staves; gunners use firearms.

Equip gear through the party menu (press Escape or M while exploring).

### Key Items

| Item | Price | Effect |
|------|-------|--------|
| Potion | 50g | Restore 50 HP |
| Hi-Potion | 200g | Restore 150 HP |
| X-Potion | 800g | Restore full HP |
| Elixir | 5,000g | Restore full HP and MP |
| Phoenix Down | 500g | Revive fallen ally at 25% HP |
| Antidote | 50g | Cure Poison |
| Remedy | 500g | Cure all status ailments |
| Smoke Bomb | 200g | Guaranteed escape from battle |
| Grenade | 300g | Deal fire damage to all enemies |

### Shops

Buy and sell at weapon shops, item shops, and magic shops. Desert shops charge 50% more than Imperial City shops. Stock up before heading to the desert.

---

## Exploration

Move through connected locations using the arrow keys or WASD. Talk to NPCs with Enter. Some NPCs offer dialogue choices that affect the story.

Random encounters occur while moving through the world and dungeons. Encounter rates vary by location -- forests and dungeons have higher rates than cities.

---

## Saving

- **Manual Save**: Open the menu and save to any of 100 slots.
- **Autosave**: The game saves automatically after each battle.
- **Quicksave**: Save instantly from the menu for a single quick-resume slot.

Save often. Some story events are permanent and cannot be undone.

---

## Status Effects

Effects last 3 turns by default unless cured.

| Effect | What It Does |
|--------|-------------|
| Poison | Lose HP each turn |
| Burn | Lose HP each turn; 15% chance to spread to adjacent enemies |
| Sleep | Skip your turn; wakes on taking damage |
| Silence | Cannot cast spells |
| Blind | Reduced accuracy |
| Paralysis | Reduced speed |
| Freeze | Cannot act for 1 turn |
| Petrify | Cannot act at all until cured |
| Berserk | Attack randomly, uncontrollable |

Cure status effects with items (Antidote, Remedy) or healing spells.

---

## Recruitment Rules

Five optional characters can be recruited. Three rules govern recruitment:

1. **Deadline**: When you agree to Orisia's "Are you ready?" question, recruitment locks permanently. Characters you missed become zombie enemies in the final battle.

2. **Fritzzit and Crankpot are paired**: They join together or not at all. Find them at the Imperial City Inn after the kobold warren but before meeting Orisia.

3. **Yipp appears only before Orisia**: Yipp spawns in random dungeon encounters. Once you meet Orisia, Yipp and his key items (Holy Symbol, Empty Pewter Wine Glass) vanish from the game.

Recruit everyone before advancing the main story past Orisia.

---

## Story Events to Watch For

These events are permanent. Know them before they happen.

- **Flood dies permanently** after the second dragon boss. No resurrection, no exception. His equipment returns to your inventory.

- **Iris goes berserk** whenever Fei drops to 0 HP in battle. She attacks randomly until Fei is revived or the battle ends. Keep Fei alive or leave Iris in reserve.

- **Yipp's alignment choice** determines your ending. Evolving Yipp into a Saint unlocks the best ending. Choosing Vampire locks you into a worse outcome -- Yipp betrays the party in the final battle.

---

## Four Endings

Your ending depends on three factors:

| Factor | How to Achieve |
|--------|---------------|
| Cure found | Complete the cure questline |
| Yipp's alignment | Evolve Yipp into Saint (not Vampire) |
| Slaver Island cleared | Defeat Captain Donald (post-credits boss) |

- **Best ending**: Cure found + Yipp is Saint + Slaver Island cleared + all 12 characters recruited.
- **Good ending**: Cure found, most characters recruited.
- **Normal ending**: Cure found, but missing several characters.
- **Bad ending**: Cure not found. Kella becomes an infected boss you must fight.

---

## Tips

- Buy Potions early. Healing with items saves MP for offense.
- Undead enemies are weak to Holy magic. Fungal enemies are weak to Fire.
- Save before entering new areas. Some story triggers are irreversible.
- Explore every dungeon before meeting Orisia to find Yipp and key items.
- Evolve your characters through Orisia's sidequests to raise their level cap to 99.
- Burn status spreads between enemies -- Crankpot's fire spells can clear groups fast.

---

## Dev Tools (Optional)

Four command-line tools ship with the desktop port for testing and debugging:

```bash
# Simulate a battle
python desktop/tools/battle_tester.py --party javin,fei --level 10 --enemies skeleton,skeleton --verbose

# View character stats at any level
python desktop/tools/stat_viewer.py --compare javin,fei --level 50

# Inspect map data
python desktop/tools/map_inspector.py --list

# View or edit save files
python desktop/tools/save_inspector.py --view 1
```
