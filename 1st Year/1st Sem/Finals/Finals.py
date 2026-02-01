import time
import random

# ============================================================================
# GLOBAL GAME STATE VARIABLES
# ============================================================================

# Player stats dictionary - stores all player information
player = {
    'name': 'Hero',
    'health': 100,
    'max_health': 100,
    'attack': 15,
    'defense': 5,
    'level': 1,
    'inventory': ['bandage', 'small health potion'],
    'gold': 50
}

# Current location tracking
current_level = 1
current_room_key = 'R1_prep'
game_over = False

# ============================================================================
# GAME DATA STRUCTURES
# ============================================================================

# Room templates - predefined room types that can be randomly selected
BASIC_ROOMS = {
    'hall': {
        'description': "A long, dusty hallway. The air is still.",
        'challenge': {'type': 'loot', 'item': 'small health potion'}
    },
    'trap': {
        'description': "A dark passage. You hear a slight click underfoot!",
        'challenge': {'type': 'trap', 'damage': 15, 'avoid_chance': 0.6}
    },
    'monster': {
        'description': "A cavernous area. A monstrous figure glares at you from the shadows!",
        'challenge': {'type': 'combat', 'enemy': {'name': 'Goblin Scoundrel', 'health': 40, 'attack': 10, 'defense': 2, 'gold': 20}}
    },
    'sanctuary': {
        'description': "A peaceful, moss-covered chamber. A soft glow emanates from a pool of water.",
        'challenge': {'type': 'heal', 'amount': 20}
    }
}

# Final boss encounter data
BOSS_FIGHT = {
    'name': 'The Dungeon Warden',
    'health': 80,
    'attack': 25,
    'defense': 8,
    'gold': 100
}

# Item definitions - what each item does when used in combat
COMBAT_ITEMS = {
    'small health potion': {'type': 'heal', 'amount': 30},
    'large health potion': {'type': 'heal', 'amount': 60},
    'bandage': {'type': 'heal', 'amount': 15},
    'attack boost': {'type': 'buff', 'stat': 'attack', 'amount': 5},
    'defense boost': {'type': 'buff', 'stat': 'defense', 'amount': 3},
    'smoke bomb': {'type': 'escape', 'chance': 0.8}
}

# Dungeon map structure - stores all rooms for each level
dungeon_map = {1: {}, 2: {}, 3: {'R3_boss': {}}}

# ============================================================================
# MAP GENERATION FUNCTIONS
# ============================================================================

def generate_dungeon_level(level_num):
    """
    Generates 3 random rooms and connects them for the given level.
    """
    room_keys = [f'R{level_num}_{i}' for i in range(1, 4)]
    
    new_level = {}
    for key in room_keys:
        room_data = random.choice(list(BASIC_ROOMS.values())).copy()
        new_level[key] = {
            'description': room_data['description'],
            'challenge': room_data['challenge'],
            'exits': {}
        }

    random.shuffle(room_keys)
    for i in range(len(room_keys) - 1):
        current, next_room = room_keys[i], room_keys[i + 1]
        new_level[current]['exits']['forward'] = next_room
    
    dungeon_map[level_num] = new_level
    return room_keys[0]

# ============================================================================
# PLAYER INTERACTION FUNCTIONS
# ============================================================================

def display_room_info():
    """
    Displays the current room's description and available exits.
    Called whenever player enters a new room.
    """
    room = dungeon_map[current_level][current_room_key]
    
    print("=" * 60)
    print(f"Level {current_level}: {current_room_key.replace('_', ' ').title()}")
    print(f"\n{room.get('description', 'A blank room.')}")
    
    print("\nExits:")
    if room['exits']:
        for direction in room['exits']:
            print(f" - {direction.capitalize()} leads deeper into the dungeon.")
    else:
        if current_level < 3:
            print(" - **[Action: DOWN]** The exit to the next level is here!") 

def go_direction():
    """
    Handles player movement between rooms.
    Since there's only forward direction, just move forward automatically.
    """
    global current_room_key
    
    room = dungeon_map[current_level][current_room_key]
    
    if not room['exits']:
        print("There are no exits to go through!")
        return
    
    target_room = room['exits']['forward']
    print(f"\nYou move forward to {target_room}...")
    current_room_key = target_room
    resolve_room_challenge()

def descend_level():
    """
    Moves player to the next dungeon level.
    Called when player finds the exit from current level.
    """
    global current_level, current_room_key
    
    print("\n" + "=" * 60)
    
    if current_level < 2:
        current_level += 1
        print(f"*** You successfully descend into **Level {current_level}**! ***")
        current_room_key = generate_dungeon_level(current_level)
        display_room_info()
    elif current_level == 2:
        current_level, current_room_key = 3, 'R3_boss'
        print("*** You hear a terrible roar. You stand before **Level 3: The Boss Chamber!** ***")
        resolve_room_challenge()

# ============================================================================
# COMBAT SYSTEM FUNCTIONS
# ============================================================================

def display_combat_ui(enemy):
    """
    Displays the combat interface with player and enemy status.
    """
    print("\n" + "=" * 60)
    print("⚔️  COMBAT  ⚔️")
    print(f"\n{player['name']}: HP {player['health']}/{player['max_health']}")
    print(f"Enemy: {enemy['name']} - HP {enemy['health']}")

def combat_action_menu():
    """
    Displays combat action menu and gets player's choice.
    """
    print("\n" + "=" * 60)
    print("COMBAT ACTIONS")
    print("\n1. FIGHT - Attack the enemy")
    print("2. ITEM - Use an item from inventory")
    print("3. MERCY - Try to spare the enemy")
    print()
    
    return input("What will you do? (1-3): ").strip()

def combat_fight(enemy):
    """
    Handle FIGHT action - player attacks enemy.
    """
    damage = max(1, player['attack'] - enemy.get('defense', 0))
    enemy['health'] -= damage
    print(f"\nYou attack {enemy['name']} for {damage} damage!")
    
    if enemy['health'] <= 0:
        gold_earned = enemy.get('gold', 10)
        player['gold'] += gold_earned
        print(f"🎉 You defeated {enemy['name']}!")
        print(f"💰 You found {gold_earned} gold! Total: {player['gold']}")
        return True
    return False

def combat_item(enemy):
    """
    Handle ITEM action - player uses item from inventory.
    """
    if not player['inventory']:
        print("\nYour inventory is empty!")
        return False
    
    combat_items = [item for item in player['inventory'] if item in COMBAT_ITEMS]
    
    if not combat_items:
        print("No usable items in combat!")
        return False
    
    print("\nYour inventory:")
    for i, item in enumerate(combat_items, 1):
        item_data = COMBAT_ITEMS[item]
        if item_data['type'] == 'heal':
            effect = f"Restores {item_data['amount']} HP"
        elif item_data['type'] == 'buff':
            effect = f"+{item_data['amount']} {item_data['stat'].title()}"
        else:
            effect = "80% chance to flee"
        print(f"{i}. {item} - {effect}")
    
    try:
        choice = int(input("\nChoose an item to use (number): ")) - 1
        if 0 <= choice < len(combat_items):
            item_used = combat_items[choice]
            item_data = COMBAT_ITEMS[item_used]
            
            if item_data['type'] == 'heal':
                player['health'] = min(player['max_health'], player['health'] + item_data['amount'])
                print(f"✨ Used {item_used}! Restored {item_data['amount']} HP. Health: {player['health']}")
            elif item_data['type'] == 'buff':
                player[item_data['stat']] += item_data['amount']
                print(f"🔮 Used {item_used}! {item_data['stat'].title()} increased by {item_data['amount']}!")
            elif item_data['type'] == 'escape':
                if random.random() < item_data['chance']:
                    print("💨 You use the smoke bomb and successfully escape!")
                    return 'fled'
                else:
                    print("❌ The smoke bomb fails! The enemy sees through your trick.")
            
            player['inventory'].remove(item_used)
        else:
            print("Invalid choice!")
    except ValueError:
        print("Please enter a valid number!")
    
    return False

def combat_mercy(enemy):
    """
    Handle MERCY action - try to spare the enemy without fighting.
    """
    if enemy['health'] == 1:
        mercy_chance = 1.0
        print("The enemy is on the brink of death and has no choice but to accept mercy!")
    else:
        mercy_chance = 0.7 if enemy['health'] < enemy.get('max_health', enemy['health']) * 0.3 else 0.3
        
        if enemy['health'] < enemy.get('max_health', enemy['health']) * 0.3:
            print("The enemy looks weakened and might accept mercy...")
    
    if random.random() < mercy_chance:
        gold_earned = enemy.get('gold', 5)
        player['gold'] += gold_earned
        print(f"💝 {enemy['name']} accepts your mercy and flees!")
        print(f"💰 They drop {gold_earned} gold as thanks! Total: {player['gold']}")
        return True
    else:
        enemy['attack'] += 2
        print(f"❌ {enemy['name']} refuses your mercy and attacks with renewed vigor!")
        return False

def enemy_turn(enemy):
    """
    Handle enemy's attack turn in combat.
    """
    print(f"\n{enemy['name']}'s turn!")
    time.sleep(1)
    
    damage = max(1, enemy['attack'] - player['defense'])
    player['health'] -= damage
    print(f"💀 {enemy['name']} attacks you for {damage} damage!")
    print(f"❤️  Your HP: {player['health']}/{player['max_health']}")
    
    if player['health'] <= 0:
        print("\n💔 You have been defeated...")
        return True
    return False

def start_combat(enemy_data):
    """
    Main combat sequence - handles the entire combat encounter.
    """
    global game_over
    
    enemy = enemy_data.copy()
    enemy['max_health'] = enemy['health']
    
    print("\n" + "=" * 60)
    print(f"⚔️  A {enemy['name']} appears! Combat initiated!")
    
    while player['health'] > 0 and enemy['health'] > 0:
        display_combat_ui(enemy)
        action = combat_action_menu()
        
        combat_over = False
        fled = False
        
        if action == '1':
            combat_over = combat_fight(enemy)
        elif action == '2':
            result = combat_item(enemy)
            if result == 'fled':
                fled = True
                combat_over = True
        elif action == '3':
            combat_over = combat_mercy(enemy)
        else:
            print("Invalid action! The enemy takes advantage of your hesitation!")
        
        if combat_over:
            break
        
        if not fled and enemy['health'] > 0:
            if enemy_turn(enemy):
                game_over = True
                break
        
        time.sleep(1)
    
    return not game_over

def resolve_room_challenge():
    """
    Handles the event or challenge in the current room.
    Called when player enters a new room with an active challenge.
    """
    global game_over
    
    room = dungeon_map[current_level][current_room_key]
    challenge = room.get('challenge')
    
    if not challenge:
        return

    if challenge['type'] == 'combat':
        if start_combat(challenge['enemy'].copy()):
            room['challenge'] = None
    elif challenge['type'] == 'trap':
        if random.random() > challenge['avoid_chance']:
            damage = challenge['damage']
            player['health'] = max(0, player['health'] - damage)
            print(f"❌ You failed to avoid the trap! You take {damage} damage!")
            if player['health'] <= 0:
                game_over = True
                print("\n💔 Your strength fails you. **GAME OVER!**")
        else:
            print("✅ You skillfully sidestep the trap! No damage taken.")
        room['challenge'] = None
    elif challenge['type'] == 'loot':
        item = challenge['item']
        player['inventory'].append(item)
        print(f"💰 You find a **{item}** and add it to your inventory.")
        room['challenge'] = None
    elif challenge['type'] == 'heal':
        heal_amount = challenge['amount']
        player['health'] = min(player['max_health'], player['health'] + heal_amount)
        print(f"✨ You rest and recover **{heal_amount}** HP. Health: {player['health']}.")
        room['challenge'] = None

# ============================================================================
# MAIN GAME FUNCTION
# ============================================================================

def main_menu():
    """
    The main entry point for the game.
    Handles initialization, main game loop, and cleanup.
    """
    global game_over, current_room_key
    
    # Setup Level 1 with preparation room
    dungeon_map[1]['R1_prep'] = {
        'description': "Welcome! You are in the **Preparation Room** (Level 1). You have 100 HP. There is an exit forward.",
        'challenge': {'type': 'loot', 'item': 'attack boost'},
        'exits': {'forward': 'R1_1'}
    }
    
    # Generate all dungeon levels
    for level in range(1, 3):
        if level > 1:
            generate_dungeon_level(level)
        else:
            room_keys = [f'R1_{i}' for i in range(1, 4)]
            new_level = {}
            
            for key in room_keys:
                room_data = random.choice(list(BASIC_ROOMS.values())).copy()
                new_level[key] = {
                    'description': room_data['description'],
                    'challenge': room_data['challenge'],
                    'exits': {}
                }

            random.shuffle(room_keys)
            for i in range(len(room_keys) - 1):
                current, next_room = room_keys[i], room_keys[i + 1]
                new_level[current]['exits']['forward'] = next_room
            
            dungeon_map[1].update(new_level)
            dungeon_map[1]['R1_prep']['exits']['forward'] = room_keys[0]
    
    # Setup boss room on Level 3
    dungeon_map[3]['R3_boss'] = {
        'description': "You stand in a vast, cold chamber. The Dungeon Warden awaits!",
        'challenge': {'type': 'combat', 'enemy': BOSS_FIGHT.copy()},
        'exits': {}
    }
    
    print("\n" + "=" * 60)
    print("      THE THREE-LEVEL ROGUELIKE DUNGEON")
    print("=" * 60)
    player['name'] = input("Enter your hero's name: ")
    print(f"Welcome, {player['name']}! Find the exit to the next level.")
    
    # Start player in preparation room and handle initial challenge
    current_room_key = 'R1_prep'
    resolve_room_challenge()

    # Main game loop
    while not game_over:
        display_room_info()
        
        room = dungeon_map[current_level][current_room_key]
        has_exits = bool(room['exits'])
        
        # Show player status and action menu
        print(f"\n[{player['name']} | HP: {player['health']}/{player['max_health']} | Gold: {player['gold']} | Lvl: {current_level}]")
        print("=========Action==============")
        
        if not has_exits and current_level < 3:
            print("1. Down - Descend to next level")
            print("2. Inv - View inventory")
            print("3. Quit - Exit game")
            action = input("\nChoose action (1-3): ").strip()
        else:
            print("1. Go - Move forward to next room") 
            print("2. Inv - View inventory")
            print("3. Quit - Exit game")
            action = input("\nChoose action (1-3): ").strip()

        # Process player actions
        if action == '1':
            if not has_exits and current_level < 3:
                descend_level()
            else:
                go_direction()
        elif action == '2':
            print(f"\nInventory: {player['inventory']}")
            print(f"Gold: {player['gold']}")
        elif action == '3':
            game_over = True
            print("You flee the dungeon. The adventure ends.")
        else:
            print("Invalid command. Please choose 1, 2, or 3.")

    # Game end sequence
    print("\n" + "=" * 60)
    if player['health'] > 0 and current_level == 3 and not dungeon_map[3]['R3_boss']['challenge']:
        print("🏆 **VICTORY!** You defeated The Dungeon Warden and escaped the dungeon!")
    elif player['health'] <= 0:
        print("The Warden laughs as you collapse. The dungeon wins this time.")
    print("=" * 60)

# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main_menu()

