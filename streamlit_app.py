import streamlit as st
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

# NHL API Base URL
NHL_API_BASE_URL = "https://api-web.nhle.com/v1/"

# Headers (if required by the API)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Helper Functions
def fetch_data(endpoint, params=None):
    """Fetch data from the NHL API with enhanced error handling."""
    url = f"{NHL_API_BASE_URL}{endpoint}"
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except ConnectionError:
        st.error("Failed to connect to the NHL API. Please check your connection.")
    except Timeout:
        st.error("The request to the NHL API timed out. Please try again later.")
    except RequestException as e:
        st.error(f"Unexpected error occurred: {e}")
    return None

def get_skater_stats_leaders(season, game_type, category=None, limit=5):
    """Retrieve skater stats leaders for a specific season and game type."""
    endpoint = f"skater-stats-leaders/{season}/{game_type}"
    params = {'categories': category, 'limit': limit}
    return fetch_data(endpoint, params)

def get_goalie_stats_leaders(season, game_type, category=None, limit=5):
    """Retrieve goalie stats leaders for a specific season and game type."""
    endpoint = f"goalie-stats-leaders/{season}/{game_type}"
    params = {'categories': category, 'limit': limit}
    return fetch_data(endpoint, params)

def get_player_game_log(player_id, season, game_type):
    """Retrieve game log for a specific player."""
    endpoint = f"player/{player_id}/game-log/{season}/{game_type}"
    return fetch_data(endpoint)

def get_player_info(player_id):
    """Retrieve detailed information for a specific player."""
    endpoint = f"player/{player_id}/landing"
    return fetch_data(endpoint)

# Streamlit App Interface
st.title("NHL Stats Explorer")
st.write("Explore skater stats leaders, goalie stats leaders, and player-specific data.")

# Skater Stats Leaders
st.header("Skater Stats Leaders")
season = st.text_input("Enter Season (YYYYYYYY format)", value="20222023")
game_type = st.selectbox("Select Game Type", options=[2, 3], format_func=lambda x: "Regular Season" if x == 2 else "Playoffs")
category = st.text_input("Enter Category (optional)", value="goals")
limit = st.number_input("Number of Results", min_value=1, max_value=50, value=5)

if st.button("Get Skater Stats Leaders"):
    skater_stats = get_skater_stats_leaders(season, game_type, category, limit)
    if skater_stats:
        st.json(skater_stats)

# Goalie Stats Leaders
st.header("Goalie Stats Leaders")
if st.button("Get Goalie Stats Leaders"):
    goalie_stats = get_goalie_stats_leaders(season, game_type, category, limit)
    if goalie_stats:
        st.json(goalie_stats)

# Player Information
st.header("Player Information")
player_id = st.text_input("Enter Player ID", value="8478402")
if st.button("Get Player Info"):
    player_info = get_player_info(player_id)
    if player_info:
        st.json(player_info)

# Player Game Log
st.header("Player Game Log")
if st.button("Get Player Game Log"):
    player_game_log = get_player_game_log(player_id, season, game_type)
    if player_game_log:
        st.json(player_game_log)
