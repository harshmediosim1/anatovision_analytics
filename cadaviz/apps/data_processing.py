import pandas as pd
import requests
import datetime
from apps.socket_manager import socketio
from apps.logger import logger

# API Endpoint
URL="http://cadaviz_web:5000/ai/analytics/data"

# Global Data Storage
existing_data = pd.DataFrame(columns=["user_id", "version", "date", "time", "location", "college", "module", "submodule", "duration"])

# User Credentials
users = {
    'Amit': 'IL17022025',  
    'Navin': 'IL16022025',  
    'Amresh': 'IL18022025' 
}
root_password = "Cadaviz@2025"

def validate_user(username, password):
    """Validate the user credentials."""
    if username in users and users[username] == password:
        logger.info(f"User {username} logged in successfully")
        return True, ""  
    elif username == "root" and password == root_password:
        logger.info("Root user logged in successfully")
        return True, ""  
    else:
        logger.warning(f"Failed login attempt for user: {username}")
        return False, "Invalid username or password"

def fetch_data():
    """Fetch data from API and update global dataset."""
    global existing_data  

    try:
        logger.info("Fetching data from API...")
        response = requests.get(URL, timeout=10)
        response.raise_for_status()  

        new_data = response.json()
        logger.info(f"API returned {len(new_data)} records.")

        if not new_data:
            logger.warning("API returned an empty dataset. No new data to update.")
            return existing_data, None  

        new_df = process_json_data(new_data)

        if new_df.empty:
            logger.warning("No valid data found after processing API response.")
            return existing_data, None  

        new_df = new_df[~new_df.isin(existing_data)].dropna()
        if not new_df.empty:
            existing_data = pd.concat([existing_data, new_df]).drop_duplicates().reset_index(drop=True)
            logger.info(f"{len(new_df)} new records added.")

            # Emit real-time update event to Dash
            socketio.emit('data_update', {'status': 'updated', 'records': len(new_df)})

        return existing_data, existing_data['date'].max() if not existing_data.empty else None  

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from API: {e}", exc_info=True)
        return existing_data, None  

    except ValueError as e:
        logger.error(f"Error decoding JSON: {e}", exc_info=True)
        return existing_data, None

    except Exception as e:
        logger.error(f"Unexpected error in fetch_data: {e}", exc_info=True)
        return existing_data, None

def create_empty_dataframe():
    """Returns an empty DataFrame with required columns."""
    logger.warning("Creating an empty DataFrame due to missing or invalid data.")
    columns = ["user_id", "version", "date", "time", "location", "college", "module", "submodule", "duration"]
    return pd.DataFrame(columns=columns)

def process_json_data(data):
    """Convert JSON response to a cleaned Pandas DataFrame."""
    try:
        if not data:
            logger.warning("No data received from API.")
            return create_empty_dataframe() 
        
        df = pd.DataFrame(data)

        # Ensure required fields exist, else assign default values
        required_columns = ["user_id", "version", "date", "time", "location", "college", "module", "submodule", "duration"]
        for col in required_columns:
            if col not in df.columns:
                df[col] = "Unknown" if col not in ["date", "duration"] else None

        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['duration'] = pd.to_numeric(df['duration'], errors='coerce').fillna(0)

        df['time'] = df['time'].astype(str).apply(lambda x: x if len(x) == 8 else x + ":00")

        logger.info(f"Data processed successfully with {len(df)} records.")
        return df
    
    except Exception as e:
        logger.error(f"Error processing data: {e}", exc_info=True)
        return create_empty_dataframe()

# Date Range for Filtering
today = datetime.date.today()
start_of_month = today.replace(day=1)
end_of_month = today.replace(day=28) + pd.DateOffset(days=4)
end_of_month = end_of_month - pd.DateOffset(days=end_of_month.day)

# Default Visualization Selection
DEFAULT_VISUALIZATIONS = ['table', 'active-users']
