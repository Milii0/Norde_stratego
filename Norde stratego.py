import streamlit as st
import random

# Define characters with their attributes, including healing and damage ignoring
characters = {
    "Elite Knight": {"HP": 33, "Speed": 3, "Base Attack": 3, "Special": "Ignores 1 damage per attack", "Heal": 0, "Damage_Ignore": 1},
    "Master Sorcerer": {"HP": 21, "Speed": 1, "Base Attack": 4, "Special": "Double damage on 2-5", "Heal": 0, "Damage_Ignore": 0},
    "Elder Druid": {"HP": 23, "Speed": 2, "Base Attack": 2, "Special": "Heals 4 HP per turn", "Heal": 4, "Damage_Ignore": 0},
    "Royal Paladin": {"HP": 27, "Speed": 4, "Base Attack": 2, "Special": "Heals 1 HP on 1 & 6 rolls", "Heal": 1, "Damage_Ignore": 0},
    "Murloc": {"HP": 15, "Speed": 6, "Base Attack": 1, "Special": "Insta Mewtwo", "Heal": 0, "Damage_Ignore": 0},
    "Mewtwo": {"HP": 40, "Speed": 5, "Base Attack": 10, "Special": "w00000t", "Heal": 0, "Damage_Ignore": 0},
}

Addons = {
    "The Immovable Object": {"HP": 3, "Speed": 0, "Base Attack": 0, "Special": "50% physical reduct", "Heal": 0, "Damage_Ignore": 0},
    "Gnomish Electric Field Deflector": {"HP": 0, "Speed": 0, "Base Attack": 0, "Special": "Counter Pika", "Heal": 0, "Damage_Ignore": 0},
    "Pikachu": {"HP": 0, "Speed": 0, "Base Attack": 12, "Special": "Cute", "Heal": 0, "Damage_Ignore": 0},
    "The Unstoppable Force": {"HP": 0, "Speed": 0, "Base Attack": 3, "Special": "Neutralize ImmObject", "Heal": 0, "Damage_Ignore": 0},
    "Rhok'delar": {"HP": 2, "Speed": 0, "Base Attack": 0, "Special": "6 to 8 kites", "Heal": 0, "Damage_Ignore": 0},
    "Frostmourne": {"HP": 0, "Speed": 0, "Base Attack": 3, "Special": "1 freezes", "Heal": 0, "Damage_Ignore": 0},
    "Defias Bandana": {"HP": 3, "Speed": 0, "Base Attack": 0, "Special": "50% physical reduct", "Heal": 0, "Damage_Ignore": 0},
    "Cloak of Shadow": {"HP": 0, "Speed": 0, "Base Attack": 0, "Special": "Vanish", "Heal": 0, "Damage_Ignore": 0},
    "Boots of Haste": {"HP": 0, "Speed": 0, "Base Attack": 0, "Special": "Change speed to 7", "Heal": 0, "Damage_Ignore": 0},
    "GM Claymore": {"HP": 0, "Speed": 0, "Base Attack": 6, "Special": "Big D", "Heal": 2, "Damage_Ignore": 0},
    "Hand of Ragnaros": {"HP": 0, "Speed": 0, "Base Attack": 2, "Special": "1,3,6 hurl fireball. 3 damage to attacker", "Heal": 0, "Damage_Ignore": 0},
    "Rocket Helmet": {"HP": 0, "Speed": 0, "Base Attack": 0, "Special": "Reduce opponents health to 17", "Heal": 0, "Damage_Ignore": 0},
}

def calculate_damage(roll, character):
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
    
    # Apply damage ignore (fighter may absorb damage)
    #attack = max(attack - character["Damage_Ignore"], 0)
    attack = roll0 + roll1 + character["Base Attack"]
    return attack

st.title("Battle Simulator")
st.write("Choose two characters to fight!")

# Initialize flags
char1_flag = False
char2_flag = False

# Select Fighter 1
char1 = st.selectbox("Select Fighter 1", list(characters.keys()))
if "last_char1" in st.session_state and st.session_state.last_char1 != char1:
    char1_flag = True
st.session_state.last_char1 = char1

# Select Fighter 2
char2 = st.selectbox("Select Fighter 2", list(characters.keys()))
if "last_char2" in st.session_state and st.session_state.last_char2 != char2:
    char2_flag = True
st.session_state.last_char2 = char2


# Initialize session state if not already initialized
if "battle_log" not in st.session_state:
    #st.write(f"DEBUG: initalised battle log")
    st.session_state.battle_log = []
    st.session_state.turn = "first"
    st.session_state.fighter1 = characters[char1].copy()
    st.session_state.fighter2 = characters[char2].copy()
    st.session_state.first_name = char1 + "1"
    st.session_state.second_name = char2 + "2"
    # Store fighter references without copying (to avoid resetting HP)
    if "first" not in st.session_state or "second" not in st.session_state:
        if st.session_state.fighter1["Speed"] > st.session_state.fighter2["Speed"]:
            st.session_state.first = st.session_state.fighter1
            st.session_state.second = st.session_state.fighter2
            st.session_state.first_name, st.session_state.second_name = char1  + "1", char2 + "2"
        else:
            st.session_state.first = st.session_state.fighter2
            st.session_state.second = st.session_state.fighter1
            st.session_state.first_name, st.session_state.second_name = char2 + "2", char1 + "1"

# Update fighter data if the selected character has changed
if char1_flag == True: #st.session_state.first_name != char1 + "1":
    char1_flag == False
    #st.write(f"DEBUG: entered char1")
    st.session_state.fighter1 = characters[char1].copy()
    st.session_state.first_name = char1 + "1"
    if st.session_state.fighter1["Speed"] > st.session_state.fighter2["Speed"]:
        st.session_state.first = st.session_state.fighter1
        st.session_state.second = st.session_state.fighter2
        st.session_state.first_name, st.session_state.second_name = char1 + "1", char2 + "2"
    else:
        st.session_state.first = st.session_state.fighter2
        st.session_state.second = st.session_state.fighter1
        st.session_state.first_name, st.session_state.second_name = char2 + "2", char1 + "1"

if char2_flag == True: #st.session_state.second_name != char2 + "2":
    char2_flag == False
    #st.write(f"DEBUG: entered char2")
    st.session_state.fighter2 = characters[char2].copy()
    st.session_state.second_name = char2 + "2"
    if st.session_state.fighter1["Speed"] > st.session_state.fighter2["Speed"]:
        st.session_state.first = st.session_state.fighter1
        st.session_state.second = st.session_state.fighter2
        st.session_state.first_name, st.session_state.second_name = char1 + "1", char2 + "2"
    else:
        st.session_state.first = st.session_state.fighter2
        st.session_state.second = st.session_state.fighter1
        st.session_state.first_name, st.session_state.second_name = char2 + "2", char1 + "1"

# Roll dice and calculate damage, apply healing and damage ignore
if st.button("Roll Dice for Current Turn"):
    if st.session_state.turn == "first":
        #If murloc fights mewtwo murloc wins (it will always be first)
        if st.session_state.first_name[:-1] == "Murloc" and st.session_state.second_name[:-1] == "Mewtwo":
            st.session_state.battle_log.append(f"{st.session_state.first_name} wins!")
        else:
            roll1 = (random.randint(1, 6), random.randint(1, 6))
            st.markdown(f"# {roll1}")
            damage1 = calculate_damage(roll1, st.session_state.first)
            st.session_state.second["HP"] -= damage1
            st.session_state.battle_log.append(f"{st.session_state.first_name} rolls {roll1} and deals {damage1} damage. {st.session_state.second_name} HP: {st.session_state.second['HP']}")

            # Apply healing for fighters with healing abilities
            if st.session_state.first_name[:-1] == "Elder Druid":
                st.session_state.first["HP"] += st.session_state.first["Heal"]
                st.session_state.battle_log.append(f"{st.session_state.first_name} heals for {st.session_state.first['Heal']} HP.")
            if st.session_state.first_name[:-1] == "Royal Paladin" and (roll1[0] in (1, 6)):
                st.session_state.first["HP"] += st.session_state.first["Heal"]
                st.session_state.battle_log.append(f"{st.session_state.first_name} heals for {st.session_state.first['Heal']} HP.")
            if st.session_state.first_name[:-1] == "Royal Paladin" and (roll1[1] in (1, 6)):
                st.session_state.first["HP"] += st.session_state.first["Heal"]
                st.session_state.battle_log.append(f"{st.session_state.first_name} heals for {st.session_state.first['Heal']} HP.")
            
            if st.session_state.second["HP"] <= 0:
                st.session_state.battle_log.append(f"{st.session_state.first_name} wins!")
        
        st.session_state.turn = "second"

    else:
        roll2 = (random.randint(1, 6), random.randint(1, 6))
        damage2 = calculate_damage(roll2, st.session_state.second)
        st.markdown(f"# {roll2}")
        st.session_state.first["HP"] -= damage2
        st.session_state.battle_log.append(f"{st.session_state.second_name} rolls {roll2} and deals {damage2} damage. {st.session_state.first_name} HP: {st.session_state.first['HP']}")

        # Apply healing for fighters with healing abilities
        if st.session_state.second_name[:-1] == "Elder Druid":
            st.session_state.second["HP"] += st.session_state.second["Heal"]
            st.session_state.battle_log.append(f"{st.session_state.second_name} heals for {st.session_state.second['Heal']} HP.")
        if st.session_state.second_name[:-1] == "Royal Paladin" and (roll2[0] in (1, 6)):
            st.session_state.second["HP"] += st.session_state.second["Heal"]
            st.session_state.battle_log.append(f"{st.session_state.second_name} heals for {st.session_state.second['Heal']} HP.")
        if st.session_state.second_name[:-1] == "Royal Paladin" and (roll2[1] in (1, 6)):
            st.session_state.second["HP"] += st.session_state.second["Heal"]
            st.session_state.battle_log.append(f"{st.session_state.second_name} heals for {st.session_state.second['Heal']} HP.")
            
        if st.session_state.first["HP"] <= 0:
            st.session_state.battle_log.append(f"{st.session_state.second_name} wins!")
        else:
            st.session_state.turn = "first"

st.markdown(f"### {st.session_state.first_name} HP: {st.session_state.first['HP']}\n ### {st.session_state.second_name} HP: {st.session_state.second['HP']}")

# Show battle log
for event in st.session_state.battle_log:
    st.write(event)

#st.write(f"DEBUG: {st.session_state}")
# Reset session state
if st.button("Reset Session"):
    st.session_state.clear()
    st.session_state.clear()

# Get memory & CPU usage
#memory = psutil.virtual_memory()
#cpu = psutil.cpu_percent(interval=1)

# Display in Streamlit
#st.write(f"**CPU Usage:** {cpu}%")
#st.write(f"**Memory Usage:** {memory.percent}%")
