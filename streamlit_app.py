import streamlit as st
import requests
import pandas as pd

# NHL Suggest API Base URL
SUGGEST_API_BASE_URL = "https://suggest.svc.nhl.com/svc/suggest/v1/minplayers/"

def search_player_by_name(name):
    """Search for players by name using the NHL Suggest API."""
    url = f"{SUGGEST_API_BASE_URL}{name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        players = data.get('suggestions', [])
        return players
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return []

def get_player_id(player_info):
    """Extract player ID from the suggestion string."""
    return player_info.split('|')[0]

def fetch_player_stats(player_id):
    """Fetch player stats using the NHL Stats API."""
    stats_api_url = f"https://statsapi.web.nhl.com/api/v1/people/{player_id}/stats?stats=careerRegularSeason"
    try:
        response = requests.get(stats_api_url)
        response.raise_for_status()
        data = response.json()
        stats = data['stats'][0]['splits'][0]['stat']
        return stats
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return {}

# Streamlit App
st.title("NHL Player Lookup")

player_name = st.text_input("Enter Player Name")

if st.button("Search"):
    if player_name:
        players = search_player_by_name(player_name)
        if players:
            player_options = {f"{p.split('|')[1]} {p.split('|')[2]}": p for p in players}
            selected_player = st.selectbox("Select a Player", list(player_options.keys()))
            player_info = player_options[selected_player]
            player_id = get_player_id(player_info)
            stats = fetch_player_stats(player_id)
            if stats:
                st.write(f"**{selected_player}**")
                st.write(f"**Games Played:** {stats.get('games', 'N/A')}")
                st.write(f"**Goals:** {stats.get('goals', 'N/A')}")
                st.write(f"**Assists:** {stats.get('assists', 'N/A')}")
                st.write(f"**Points:** {stats.get('points', 'N/A')}")
            else:
                st.write("No stats available for this player.")
        else:
            st.write("No players found with that name.")
    else:
        st.write("Please enter a player name.")
