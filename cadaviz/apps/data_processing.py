import pandas as pd
import requests
import datetime
from apps.socket_manager import socketio  # Import socketio from app.py

# API Endpoint
URL="http://cadaviz_web:5000/ai/analytics/data"

existing_data = pd.DataFrame()

users = {
    'Amit': 'IL17022025',  
    'Navin': 'IL16022025',  
    'Amresh': 'IL18022025' 
}

root_password = "Cadaviz@2025"

def validate_user(username, password):
    """Validate the user credentials."""
    if username in users and users[username] == password:
        return True, ""  
    elif username == "root" and password == root_password:
        return True, ""  
    else:
        return False, "Invalid username or password"

def fetch_data():
    """Fetch data from API, append new records without removing existing data, and trigger real-time updates."""
    global existing_data  

    try:
        response = requests.get(URL)
        response.raise_for_status()  
        
        new_data = response.json() 
        new_df = process_json_data(new_data)

        if not new_df.empty:
            new_df = new_df[~new_df.isin(existing_data)].dropna()
            if not new_df.empty:
                existing_data = pd.concat([existing_data, new_df]).drop_duplicates().reset_index(drop=True)

                # 🔹 Emit real-time update event to Dash
                socketio.emit('data_update', {'status': 'updated', 'records': len(new_df)})
        
        latest_update_time = existing_data['date'].max() if not existing_data.empty else None  
        return existing_data, latest_update_time  

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the API: {e}")
        return existing_data, None  

    except ValueError as e:
        print(f"Error decoding JSON: {e}")
        return existing_data, None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return existing_data, None

def create_empty_dataframe():
    """Returns an empty DataFrame with required columns to prevent crashes."""
    columns = ["user_id", "version", "date", "time", "location", "college", "module", "submodule", "duration"]
    return pd.DataFrame(columns=columns)

def process_json_data(data):
    """Convert JSON response to a cleaned Pandas DataFrame."""
    try:
        if not data:
            return create_empty_dataframe() 
        
        df = pd.DataFrame(data)
        df['user_id'] = df.get('user_id', 'Unknown')
        df['date'] = pd.to_datetime(df.get('date'), errors='coerce')
        
        # 🔹 Fix inconsistent time format (add seconds if missing)
        df['time'] = df.get('time', '').astype(str)
        df['time'] = df['time'].apply(lambda x: x if len(x) == 8 else x + ":00")
        
        df['college'] = df.get('college', "Unknown")
        return df
    
    except Exception as e:
        print(f"Error processing data: {e}")
        return create_empty_dataframe()

today = datetime.date.today()
start_of_month = today.replace(day=1)
end_of_month = today.replace(day=28) + pd.DateOffset(days=4)  
end_of_month = end_of_month - pd.DateOffset(days=end_of_month.day)  

# Default visualization selection
DEFAULT_VISUALIZATIONS = ['table', 'active-users']
