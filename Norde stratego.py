import streamlit as st
import random
# Initialize flags
char1_flag = False
char2_flag = False
item1_flag = False
item2_flag = False
skip_turn = False

# Define characters with their attributes, including healing and damage ignoring
characters = {
    "Elite Knight": {"HP": 33, "Speed": 3, "Base Attack": 3, "Special": "Ignores 1 damage per attack", "Heal": 0, "Damage_Ignore": 1},
    "Master Sorcerer": {"HP": 21, "Speed": 1, "Base Attack": 4, "Special": "Double damage on 2-5", "Heal": 0, "Damage_Ignore": 0},
    "Elder Druid": {"HP": 23, "Speed": 2, "Base Attack": 2, "Special": "Heals 4 HP per turn", "Heal": 4, "Damage_Ignore": 0},
    "Royal Paladin": {"HP": 27, "Speed": 4, "Base Attack": 2, "Special": "Heals 1 HP on 1 & 6 rolls", "Heal": 1, "Damage_Ignore": 0},
    "Murloc": {"HP": 15, "Speed": 6, "Base Attack": 1, "Special": "Insta Mewtwo", "Heal": 0, "Damage_Ignore": 0},
    "Mewtwo": {"HP": 40, "Speed": 5, "Base Attack": 10, "Special": "w00000t", "Heal": 0, "Damage_Ignore": 0},
}

addons = {
    "The Immovable Object": {"HP": 0, "Speed": 0, "Base Attack": 0, "Special": "50% physical reduct", "Heal": 0, "Damage_Ignore": 0},
    "Gnomish Electric Field Deflector": {"HP": 0, "Speed": 0, "Base Attack": 0, "Special": "Counter Pika", "Heal": 0, "Damage_Ignore": 0},
    "Pikachu": {"HP": 0, "Speed": 0, "Base Attack": 0, "Special": "Cute", "Heal": 0, "Damage_Ignore": 0},
    "The Unstoppable Force": {"HP": 0, "Speed": 0, "Base Attack": 0, "Special": "Neutralize ImmObject", "Heal": 0, "Damage_Ignore": 0},
    "Rhok'delar": {"HP": 2, "Speed": 0, "Base Attack": 0, "Special": "6 to 8 kites", "Heal": 0, "Damage_Ignore": 0},
    "Frostmourne": {"HP": 0, "Speed": 0, "Base Attack": 0, "Special": "1 freezes", "Heal": 0, "Damage_Ignore": 0},
    "Defias Bandana": {"HP": 0, "Speed": 0, "Base Attack": 0, "Special": "No damage taken on 4, 6", "Heal": 0, "Damage_Ignore": 0},
    "Cloak of Shadow": {"HP": 0, "Speed": 0, "Base Attack": 0, "Special": "Vanish", "Heal": 0, "Damage_Ignore": 0},
    "Boots of Haste": {"HP": 0, "Speed": 0, "Base Attack": 0, "Special": "Change speed to 7", "Heal": 0, "Damage_Ignore": 0},
    "GM Claymore": {"HP": 0, "Speed": 0, "Base Attack": 0, "Special": "Big D", "Heal": 0, "Damage_Ignore": 0},
    "Hand of Ragnaros": {"HP": 0, "Speed": 0, "Base Attack": 0, "Special": "1,3,6 hurl fireball. 3 damage to attacker", "Heal": 0, "Damage_Ignore": 0},
    "Rocket Helmet": {"HP": 0, "Speed": 0, "Base Attack": 0, "Special": "Reduce opponents health to 17", "Heal": 0, "Damage_Ignore": 0},
}
def apply_rocket_helmet_effect(item, opponent_name):
    if "Rocket Helmet" in item:
        HP = 17
        st.session_state.battle_log.append(f"Rocket Helmet reduced {opponent_name} health to 17!")
    return HP

def calculate_healing(roll, character, heal): #add weapon?
    healing = 0

    if character[:-1] == "Elder Druid":
        healing += heal
    if character[:-1] == "Royal Paladin" and (roll[0] in (1, 6)):
        healing += heal
    if character[:-1] == "Royal Paladin" and (roll[1] in (1, 6)):
        healing += heal
    
    return healing

def calculate_damage(roll, character, character_name, attack_item, defend_item):
    skip = False
    st.write(f"{roll}, {character}, {character_name}, {attack_item}, {defend_item}")
    if character["Special"] == "Double damage on 2-5":
        if roll[0] in (2, 3, 4, 5):
            roll0 = roll[0] * 2
        else:
            roll0 = roll[0]
        if roll[1] in (2, 3, 4, 5):
            roll1 = roll[1] * 2
        else:
            roll1 = roll[1]
    else:
        roll0 = roll[0]
        roll1 = roll[1]
    
    if "Defias Bandana" in defend_item and (roll[0] in (4, 6) or roll[1] in (4, 6)):
        roll0 = 0
        roll1 = 0
        st.session_state.battle_log.append(f"Defias Bandana blocks damage from roll!")

    # Apply damage ignore (fighter may absorb damage)
    #attack = max(attack - character["Damage_Ignore"], 0)
    attack = roll0 + roll1 + character["Base Attack"]

    #Immovable object vs unstoppable force effects
    if "The Immovable Object" in attack_item:
        if "The Unstoppable Force" in defend_item: 
            st.session_state.battle_log.append(f"The Unstoppable Force meets the Immovable object! All effects cancel..")
    if "The Immovable Object" in defend_item and character_name in ["Elite Knight", "Royal Paladin"]:
        if "The Unstoppable Force" in attack_item:
            st.session_state.battle_log.append("The Unstoppable Force meets the Immovable object! All effects cancel..")
        else:
            attack //= 2
            st.session_state.battle_log.append("The enemy blocked half your damage!!")

    if "The Unstoppable Force" in attack_item: 
        if "The Immovable Object" in defend_item:
            attack = attack
        else:
            attack += 3
            st.session_state.battle_log.append(f"The Unstoppable Force adds 3 damage to your attack!")

    #Pikachu and E field deflector effect
    if attack_item == "Pikachu" and defend_item != "Gnomish Electric Field Deflector":
        attack += 12
        st.session_state.battle_log.append(f"Pikachu blasts Thunderbolt for 12 damage!!")
    if attack_item == "Pikachu" and defend_item == "Gnomish Electric Field Deflector":
        st.session_state.battle_log.append(f"Pikachu blasts himself for 12 damage :O")
        #add minus damage  

        
    # Add damage to attacker if needed
    if attack_item == "Hand of Ragnaros":
        if roll[0] in (1, 3, 6):
            attack += 3
            st.session_state.battle_log.append(f"A giant fireball hurls towards your enemy, dealing 3 damage")
        if roll[1] in (1, 3, 6):
            attack += 3
            st.session_state.battle_log.append(f"A giant fireball hurls towards your enemy, dealing 3 damage")
    
    if "GM Claymore" in attack_item:
        attack += 6
        st.session_state.battle_log.append(f"Grand Marshals Claymore adds 6 damage to your attack!")

    if "Frostmourne" in attack_item:
        attack += 3
        if roll[0] == 1 or roll[1] == 1:
            st.session_state.battle_log.append(f"Frostmourne freezes your opponent, and add 3 damage!")
            skip = True #turskifte
        else:
            st.session_state.battle_log.append(f"Frostmourne adds 3 extra damage!")

    if "Rhok'delar" in attack_item:
        if (roll[0]+roll[1]) in (6, 7, 8):
            st.session_state.battle_log.append(f"You kite your opponent with Rhok'delar!")
            skip = True #turskifte
        else:
            st.session_state.battle_log.append(f"Rhok'delar misses :(")


    return attack, skip

#def item_effect(attack_item, enemy_type, defend_item)
    #if attack_item is "50% physical reduct" and enemy_type is "Elite Knight" or "Royal Paladin"

st.title("Battle Simulator")
st.write("Choose two characters to fight!")

# Select Fighter 1
char1 = st.selectbox("Select Fighter 1", list(characters.keys()))
item1 = st.selectbox("Select item for Fighter 1", list(addons.keys()))
if "last_char1" in st.session_state and st.session_state.last_char1 != char1:
    char1_flag = True
if "last_item1" in st.session_state and st.session_state.last_item1 != item1:
    item1_flag = True
st.session_state.last_char1 = char1
st.session_state.last_item1 = item1

# Select Fighter 2
char2 = st.selectbox("Select Fighter 2", list(characters.keys()))
item2 = st.selectbox("Select item for Fighter 2", list(addons.keys()))
if "last_char2" in st.session_state and st.session_state.last_char2 != char2:
    char2_flag = True
if "last_item2" in st.session_state and st.session_state.last_item2 != item2:
    item2_flag = True
st.session_state.last_char2 = char2
st.session_state.last_item2 = item2


# Initialize session state if not already initialized
if "battle_log" not in st.session_state:
    #st.write(f"DEBUG: initalised battle log")
    st.session_state.battle_log = []
    st.session_state.turn = "first"
    st.session_state.round = 1
    st.session_state.fighter1 = characters[char1].copy()
    st.session_state.fighter2 = characters[char2].copy()
    st.session_state.first_name = char1 + "1"
    st.session_state.second_name = char2 + "2"
    st.session_state.fighter1_item = item1
    st.session_state.fighter2_item = item2
    if "Boots of Haste" in st.session_state.fighter1_item:
        st.session_state.fighter1["Speed"] = 7
    if "Boots of Haste" in st.session_state.fighter2_item:
        st.session_state.fighter2["Speed"] = 7

    # Store fighter references without copying (to avoid resetting HP)
    if "first" not in st.session_state or "second" not in st.session_state:
        if st.session_state.fighter1["Speed"] > st.session_state.fighter2["Speed"]:
            st.session_state.first = st.session_state.fighter1
            st.session_state.first_item, st.session_state.second_item = st.session_state.fighter1_item, st.session_state.fighter2_item
            st.session_state.second = st.session_state.fighter2
            st.session_state.first_name, st.session_state.second_name = char1  + "1", char2 + "2"
        else:
            st.session_state.first = st.session_state.fighter2
            st.session_state.first_item, st.session_state.second_item = st.session_state.fighter2_item, st.session_state.fighter1_item
            st.session_state.second = st.session_state.fighter1
            st.session_state.first_name, st.session_state.second_name = char2 + "2", char1 + "1"

# Update fighter data if the selected character has changed
if char1_flag == True or item1_flag == True: #st.session_state.first_name != char1 + "1":
    char1_flag == False
    item1_flag == False
    #st.write(f"DEBUG: entered char1")
    st.session_state.fighter1 = characters[char1].copy()
    st.session_state.first_name = char1 + "1"
    st.session_state.fighter1_item = item1
    if "Boots of Haste" in st.session_state.fighter1_item:
        st.session_state.fighter1["Speed"] = 7
    if "Boots of Haste" in st.session_state.fighter2_item:
        st.session_state.fighter2["Speed"] = 7

    if st.session_state.fighter1["Speed"] > st.session_state.fighter2["Speed"]:
        st.session_state.first = st.session_state.fighter1
        st.session_state.first_item, st.session_state.second_item = st.session_state.fighter1_item, st.session_state.fighter2_item
        st.session_state.second = st.session_state.fighter2
        st.session_state.first_name, st.session_state.second_name = char1 + "1", char2 + "2"
    else:
        st.session_state.first = st.session_state.fighter2
        st.session_state.first_item, st.session_state.second_item = st.session_state.fighter2_item, st.session_state.fighter1_item
        st.session_state.second = st.session_state.fighter1
        st.session_state.first_name, st.session_state.second_name = char2 + "2", char1 + "1"

if char2_flag == True or item2_flag == True: #st.session_state.second_name != char2 + "2":
    char2_flag == False
    item2_flag == False
    #st.write(f"DEBUG: entered char2")
    st.session_state.fighter2 = characters[char2].copy()
    st.session_state.second_name = char2 + "2"
    st.session_state.fighter2_item = item2
    if "Boots of Haste" in st.session_state.fighter1_item:
        st.session_state.fighter1["Speed"] = 7
    if "Boots of Haste" in st.session_state.fighter2_item:
        st.session_state.fighter2["Speed"] = 7
    if st.session_state.fighter1["Speed"] > st.session_state.fighter2["Speed"]:
        st.session_state.first = st.session_state.fighter1
        st.session_state.first_item, st.session_state.second_item = st.session_state.fighter1_item, st.session_state.fighter2_item
        st.session_state.second = st.session_state.fighter2
        st.session_state.first_name, st.session_state.second_name = char1 + "1", char2 + "2"
    else:
        st.session_state.first = st.session_state.fighter2
        st.session_state.first_item, st.session_state.second_item = st.session_state.fighter2_item, st.session_state.fighter1_item
        st.session_state.second = st.session_state.fighter1
        st.session_state.first_name, st.session_state.second_name = char2 + "2", char1 + "1"

# Roll dice and calculate damage, apply healing and damage ignore
if st.button("Roll Dice for Current Turn"):
    #If one fighter has rocket helm, reduce opponents HP
    if st.session_state.round == 1 and st.session_state.turn == "first":
        if "Rocket Helmet" in st.session_state.fighter1_item:
            if st.session_state.fighter1 == st.session_state.first:
                st.session_state.second["HP"] = 17
                st.session_state.battle_log.append(f"Rocket Helmet reduced {st.session_state.second_name} health to 17!")
            else:
                st.session_state.first["HP"] = 17
                st.session_state.battle_log.append(f"Rocket Helmet reduced {st.session_state.first_name} health to 17!")
        if "Rocket Helmet" in st.session_state.fighter2_item:
            if st.session_state.fighter2 == st.session_state.first:
                st.session_state.second["HP"] = 17
                st.session_state.battle_log.append(f"Rocket Helmet reduced {st.session_state.second_name} health to 17!")
            if st.session_state.fighter2 == st.session_state.second:
                st.session_state.first["HP"] = 17
                st.session_state.battle_log.append(f"Rocket Helmet reduced {st.session_state.first_name} health to 17!")

    if st.session_state.turn == "first":
        st.session_state.battle_log.append(f"Round {st.session_state.round}: {st.session_state.first_name}")
        #If murloc fights mewtwo murloc wins (it will always be first)
        if st.session_state.first_name[:-1] == "Murloc" and st.session_state.second_name[:-1] == "Mewtwo":
            st.session_state.battle_log.append(f"{st.session_state.first_name} wins!")
        
        roll1 = (random.randint(1, 6), random.randint(1, 6))
        st.markdown(f"# {roll1}")
        damage1, skip_turn = calculate_damage(roll1, st.session_state.first, st.session_state.first_name, st.session_state.first_item, st.session_state.second_item)
        st.session_state.second["HP"] -= damage1
        st.session_state.battle_log.append(f"{st.session_state.first_name} rolls {roll1} and deals {damage1} damage. {st.session_state.second_name} HP: {st.session_state.second['HP']}")

        # Apply healing for fighters with healing abilities
        healing1 = calculate_healing(roll1, st.session_state.first_name, st.session_state.first["Heal"])
        st.session_state.first["HP"] += healing1
        if healing1 > 0:
            st.session_state.battle_log.append(f"{st.session_state.first_name} heals for {healing1} HP.")
        
        #On death declare winner
        if st.session_state.second["HP"] <= 0:
            st.session_state.battle_log.append(f"{st.session_state.first_name} wins!")
        
        if skip_turn == True:
            st.session_state.turn = "first"
            st.session_state.round += 1
        else:
            st.session_state.turn = "second"

    else:
        st.session_state.battle_log.append(f"Round {st.session_state.round}: {st.session_state.second_name}")
        roll2 = (random.randint(1, 6), random.randint(1, 6))
        damage2, skip_turn = calculate_damage(roll2, st.session_state.second, st.session_state.second_name, st.session_state.second_item, st.session_state.first_item)
        st.markdown(f"# {roll2}")
        st.session_state.first["HP"] -= damage2
        st.session_state.battle_log.append(f"{st.session_state.second_name} rolls {roll2} and deals {damage2} damage. {st.session_state.first_name} HP: {st.session_state.first['HP']}")

        # Apply healing for fighters with healing abilities
        healing2 = calculate_healing(roll2, st.session_state.second_name, st.session_state.second["Heal"])
        st.session_state.second["HP"] += healing2
        if healing2 > 0:
            st.session_state.battle_log.append(f"{st.session_state.second_name} heals for {healing2} HP.")

        #on death declare winner    
        if st.session_state.first["HP"] <= 0:
            st.session_state.battle_log.append(f"{st.session_state.second_name} wins!")
        
        if skip_turn == True:
            st.session_state.turn = "second"
            st.session_state.round += 1
        else:
            st.session_state.turn = "first"
            st.session_state.round += 1

st.markdown(f"### {st.session_state.first_name} HP: {st.session_state.first['HP']}\n ### {st.session_state.second_name} HP: {st.session_state.second['HP']}")

# Show battle log
for event in st.session_state.battle_log:
    st.write(event)

#st.write(f"DEBUG: {st.session_state}")
# Reset session state
if st.button("Reset Session"):
    st.session_state.clear()
    st.session_state.clear()
