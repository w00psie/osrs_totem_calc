import math
import streamlit as st
from levels import xp_to_level, level_to_xp
from helpers import (
    TIME,
    Action,
    Item,
    calc_totem_xp,
    calc_chance,
    calc_time,
    con_xp,
    Material,
    FLETCHING_STUFF,
    Axe,
)
import requests

url = "https://api.wiseoldman.net/v2"
headers = {"Content-Type": "application/json"}


# Just format options by using the enum value in title case
def format_option_title_case(option):
    return option.value.title()


st.set_page_config(page_title="OSRS Vale Totem Calculator")
st.title("Totem Calculator")
# Make 3 columns for inputs
player_fletch_xp = 0
player_construction_xp = 0
player_woodcutting_lvl = 1
input_name = st.text_input(label="In Game Name")
if input_name:
    # get from wiseoldman
    try:
        player_data = (
            requests.post(url + f"/players/{input_name}", headers=headers)
            .json()
            .get("latestSnapshot")
            .get("data")
        )
        if player_data:
            player_fletch_xp = (
                player_data.get("skills").get("fletching").get("experience")
            )
            player_construction_xp = (
                player_data.get("skills").get("construction").get("experience")
            )
            player_woodcutting_lvl = (
                player_data.get("skills").get("woodcutting").get("level")
            )
    except Exception as e:
        print(e)

input_col1, input_col2, input_col3 = st.columns(3)

with input_col1:
    curr_fletching_xp = st.number_input(
        label="Current Fletching XP",
        min_value=0,
        value=(player_fletch_xp),
        max_value=level_to_xp(99),
    )
with input_col2:
    curr_woodcutting_lvl = st.number_input(
        label="Current Woodcutting Level",
        min_value=1,
        max_value=99,
        value=player_woodcutting_lvl,
    )
with input_col3:
    curr_con_xp = st.number_input(
        label="Current Construction XP",
        min_value=0,
        value=player_construction_xp,
        max_value=level_to_xp(99),
    )


col1, col2 = st.columns(2)
# Get target Fletching Level
with col1:
    target = st.number_input(
        label="Target Fletching Level", min_value=1, max_value=99, value=99
    )
with col2:
    axe_type = st.selectbox(
        "Choose an axe:",
        options=[a for a in Axe],
        format_func=format_option_title_case,
    )
# Calculate XP difference
xp_diff = level_to_xp(target) - curr_fletching_xp

# Get material of items
with col1:
    material = st.selectbox(
        "Choose a material:",
        options=[m for m in Material],
        format_func=format_option_title_case,
    )
# Get fletched item
with col2:
    item = st.selectbox(
        "Choose an item:",
        options=[i for i in FLETCHING_STUFF.get(material, {}).get("Items", [])],
        format_func=format_option_title_case,
    )

# Calc how much xp per totem with material + item
totem_xp = calc_totem_xp(material, item)

# Results
# How many totems ya need?
totems_needed = math.ceil(xp_diff / totem_xp)
items_needed = totems_needed * 4

logs_needed = items_needed + totems_needed

if item == Item.SHIELD:
    logs_needed = (items_needed * 2) + totems_needed
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Totems Needed:", value=f"{totems_needed:,}")

with col2:
    st.metric(
        label="Logs Needed:",
        value=f"{logs_needed:,}",
    )
with col3:
    st.metric(label="Items Needed:", value=f"{items_needed:,}")

time_needed_cutting = calc_time(
    logs_needed, axe_type, material, curr_woodcutting_lvl, item
)
time_needed_fletching = (items_needed * TIME.get(item)) / 3600
with st.container():
    st.header("Time Needed")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Time Needed to cut logs:",
            value=f"{(time_needed_cutting):.1f} hours",
        )
    with col2:
        st.metric(
            label="Time to fletch:",
            value=f"{(time_needed_fletching):.1f} hours",
            help="Does not take fletching knife into account",
        )
with st.container():
    st.header("XP Gained")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Construction XP gained",
            value=f"{(con_xp(xp_to_level(curr_con_xp), totems_needed)):,}",
        )
    with col2:
        st.metric(
            "Woodcutting XP gained:",
            value=f"{(FLETCHING_STUFF[material][Action.CUT] * logs_needed):,}",
        )
