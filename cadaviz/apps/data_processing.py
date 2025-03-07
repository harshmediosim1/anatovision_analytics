import pandas as pd
import requests
from apps.socket_manager import socketio
from apps.logger import logger

URL = "http://cadaviz_web:5000/ai/analytics/data"

existing_data = pd.DataFrame(columns=[
    "user_id", "version", "date", "time", "location", "college", 
    "module", "submodule", "duration"
])

users = {
    'Amit': 'IL17022025',  
    'Navin': 'IL16022025',  
    'Amresh': 'IL18022025' 
}
root_password = "Cadaviz@2025"

def validate_user(username, password):
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
    global existing_data  

    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()  
        new_data = response.json()

        if not new_data:
            return existing_data, None  

        new_df = process_json_data(new_data)

        if new_df.empty:
            return existing_data, None  

        combined_data = pd.concat([existing_data, new_df]).reset_index(drop=True)
       # combined_data.sort_values(by=['date', 'time'], ascending=[False, False], inplace=True)
        new_rows = combined_data.iloc[len(existing_data):]

        if not new_rows.empty:
            existing_data = combined_data  
            for _, row in new_rows.iterrows():
                socketio.emit('data_update', {'status': 'new_row', 'row': row.to_dict()}, to='/')

        return existing_data, existing_data['date'].max() if not existing_data.empty else None  

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data: {e}", exc_info=True)
        return existing_data, None  
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return existing_data, None

def create_empty_dataframe():
    columns = ["user_id", "version", "date", "time", "location", "college", "module", "submodule", "duration"]
    return pd.DataFrame(columns=columns)

def process_json_data(data):
    try:
        if not data:
            return create_empty_dataframe() 
        
        df = pd.DataFrame(data)

        required_columns = ["user_id", "version", "date", "time", "location", "college", "module", "submodule", "duration"]
        for col in required_columns:
            if col not in df.columns:
                df[col] = "Unknown" if col not in ["date", "duration"] else None

        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['duration'] = pd.to_numeric(df['duration'], errors='coerce').fillna(0)
        df['time'] = df['time'].astype(str).apply(lambda x: x if len(x) == 8 else x + ":00")

        return df
    
    except Exception as e:
        logger.error(f"Error processing data: {e}", exc_info=True)
        return create_empty_dataframe()

DEFAULT_VISUALIZATIONS = ['table', 'active-users']