import streamlit as st
import random

# Define characters with their attributes, including healing and damage ignoring
characters = {
    "Elite Knight": {"HP": 33, "Speed": 3, "Base Attack": 3, "Special": "Ignores 1 damage per attack", "Heal": 0, "Damage_Ignore": 1},
    "Master Sorcerer": {"HP": 21, "Speed": 1, "Base Attack": 4, "Special": "Double damage on 2-5", "Heal": 0, "Damage_Ignore": 0},
    "Elder Druid": {"HP": 23, "Speed": 2, "Base Attack": 2, "Special": "Heals 4 HP per turn", "Heal": 4, "Damage_Ignore": 0},
    "Royal Paladin": {"HP": 27, "Speed": 4, "Base Attack": 2, "Special": "Heals 1 HP on 1 & 6 rolls", "Heal": 1, "Damage_Ignore": 0},
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

# Select Fighter 1 and Fighter 2
char1 = st.selectbox("Select Fighter 1", list(characters.keys()))
char2 = st.selectbox("Select Fighter 2", list(characters.keys()))

# Initialize session state if not already initialized
if "battle_log" not in st.session_state:
    st.session_state.battle_log = []
    st.session_state.turn = "first"

# Update fighter data if not already stored in session state
if "fighter1" not in st.session_state or st.session_state.first_name != char1:
    st.session_state.fighter1 = characters[char1].copy()
    st.session_state.first_name = char1

if "fighter2" not in st.session_state or st.session_state.second_name != char2:
    st.session_state.fighter2 = characters[char2].copy()
    st.session_state.second_name = char2

# Store fighter references without copying (to avoid resetting HP)
if "first" not in st.session_state or "second" not in st.session_state:
    if st.session_state.fighter1["Speed"] > st.session_state.fighter2["Speed"]:
        st.session_state.first = st.session_state.fighter1
        st.session_state.second = st.session_state.fighter2
        st.session_state.first_name, st.session_state.second_name = char1, char2
    else:
        st.session_state.first = st.session_state.fighter2
        st.session_state.second = st.session_state.fighter1
        st.session_state.first_name, st.session_state.second_name = char2, char1


# Roll dice and calculate damage, apply healing and damage ignore
if st.button("Roll Dice for Current Turn"):
    if st.session_state.turn == "first":
        roll1 = (random.randint(1, 6), random.randint(1, 6))
        damage1 = calculate_damage(roll1, st.session_state.first)
        st.session_state.second["HP"] -= damage1
        st.session_state.battle_log.append(f"{st.session_state.first_name} rolls {roll1} and deals {damage1} damage. {st.session_state.second_name} HP: {st.session_state.second['HP']}")

        # Apply healing for fighters with healing abilities
        if st.session_state.first_name == "Elder Druid":
            st.session_state.first["HP"] += st.session_state.first["Heal"]
            st.session_state.battle_log.append(f"{st.session_state.first_name} heals for {st.session_state.first['Heal']} HP.")
        if st.session_state.first_name == "Royal Paladin" and (roll1[0] in (1, 6)):
            st.session_state.first["HP"] += st.session_state.first["Heal"]
            st.session_state.battle_log.append(f"{st.session_state.first_name} heals for {st.session_state.first['Heal']} HP.")
        if st.session_state.first_name == "Royal Paladin" and (roll1[1] in (1, 6)):
            st.session_state.first["HP"] += st.session_state.first["Heal"]
            st.session_state.battle_log.append(f"{st.session_state.first_name} heals for {st.session_state.first['Heal']} HP.")
        
        if st.session_state.second["HP"] <= 0:
            st.session_state.battle_log.append(f"{st.session_state.first_name} wins!")
        else:
            st.session_state.turn = "second"
    else:
        roll2 = (random.randint(1, 6), random.randint(1, 6))
        damage2 = calculate_damage(roll2, st.session_state.second)
        st.session_state.first["HP"] -= damage2
        st.session_state.battle_log.append(f"{st.session_state.second_name} rolls {roll2} and deals {damage2} damage. {st.session_state.first_name} HP: {st.session_state.first['HP']}")

        # Apply healing for fighters with healing abilities
        if st.session_state.second_name == "Elder Druid":
            st.session_state.second["HP"] += st.session_state.second["Heal"]
            st.session_state.battle_log.append(f"{st.session_state.second_name} heals for {st.session_state.second['Heal']} HP.")
        if st.session_state.second_name == "Royal Paladin" and (roll2[0] in (1, 6)):
            st.session_state.second["HP"] += st.session_state.second["Heal"]
            st.session_state.battle_log.append(f"{st.session_state.second_name} heals for {st.session_state.second['Heal']} HP.")
        if st.session_state.second_name == "Royal Paladin" and (roll2[1] in (1, 6)):
            st.session_state.second["HP"] += st.session_state.second["Heal"]
            st.session_state.battle_log.append(f"{st.session_state.second_name} heals for {st.session_state.second['Heal']} HP.")
            
        if st.session_state.first["HP"] <= 0:
            st.session_state.battle_log.append(f"{st.session_state.second_name} wins!")
        else:
            st.session_state.turn = "first"

st.write(f"Status: {st.session_state.first_name} HP: {st.session_state.first['HP']}, {st.session_state.second_name} HP: {st.session_state.second['HP']}")

# Show battle log
for event in st.session_state.battle_log:
    st.write(event)

# Reset session state
if st.button("Reset Session"):
    st.session_state.clear()