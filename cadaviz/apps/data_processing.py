import pandas as pd
import requests
import datetime

# API Endpoint
URL = "https://b997-2401-4900-1c43-73c5-ac38-d042-d7e8-6b3c.ngrok-free.app/ai/analytics/data"

def fetch_data():
    """Fetch data from API and return a cleaned DataFrame."""
    response = requests.get(URL)
    
    if response.status_code == 200:
        data = response.json()  # Assuming data is a JSON list of records
    else:
        data = []

    return process_json_data(data)

def process_json_data(data):
    """Convert JSON response to a cleaned Pandas DataFrame."""
    if not data:
        return pd.DataFrame()  # Return an empty DataFrame if no data

    df = pd.DataFrame(data)

    # Ensure 'user_id' column is present (handle missing column case)
    df['user_id'] = df.get('user_id', 'Unknown')

    # Ensure 'date' column exists and is in datetime format
    df['date'] = pd.to_datetime(df.get('date'), errors='coerce')

    # Ensure 'time' column exists and is a string
    df['time'] = df.get('time', '').astype(str)

    # Ensure 'college' column is present
    df['college'] = df.get('college', "Unknown")

    return df

# Get the current month start and end date
today = datetime.date.today()
start_of_month = today.replace(day=1)
end_of_month = today.replace(day=28) + pd.DateOffset(days=4)  # Moves to last day of month
end_of_month = end_of_month - pd.DateOffset(days=end_of_month.day)

# Default visualization selection
DEFAULT_VISUALIZATIONS = ['table', 'active-users']
