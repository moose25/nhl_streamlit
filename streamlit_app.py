import streamlit as st
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

# NHL API Base URL (Direct Connection)
NHL_API_BASE_URL = "https://statsapi.web.nhl.com/api/v1/"

# User-Agent Header
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Helper Functions
def fetch_data(endpoint):
    """Fetch data from the NHL API with enhanced error handling."""
    url = f"{NHL_API_BASE_URL}{endpoint}"
    try:
        st.write(f"Attempting to fetch data from: {url}")  # Debug log
        response = requests.get(url, headers=HEADERS, timeout=10)  # Direct request
        st.write(f"Response Status: {response.status_code}")  # Debug log
        response.raise_for_status()
        return response.json()
    except ConnectionError:
        st.error("Failed to connect to the NHL API. Please check your connection.")
    except Timeout:
        st.error("The request to the NHL API timed out. Please try again later.")
    except RequestException as e:
        st.error(f"Unexpected error occurred: {e}")
    return None

def get_teams():
    """Retrieve all NHL teams."""
    data = fetch_data("teams")
    if data and "teams" in data:
        return data["teams"]
    return []

# Streamlit App Interface
st.title("NHL Teams & Player Stats")
st.write("Explore NHL teams, view their rosters, team stats, and player stats.")

# Fetch NHL teams
teams = get_teams()
if teams:
    team_names = [team["name"] for team in teams]
    selected_team = st.selectbox("Select a Team", team_names)
else:
    st.error("Failed to fetch NHL teams. Please try again later.")
