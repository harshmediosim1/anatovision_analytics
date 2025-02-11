import pandas as pd
import requests
import datetime

# API Endpoint
URL = "http://cadaviz_web:5000/ai/analytics/data"

def fetch_data():
    """Fetch data from API and return a cleaned DataFrame."""
    try:
        response = requests.get(URL)
        response.raise_for_status() 
        
        data = response.json()  # Assuming data is a JSON list of records

        return process_json_data(data)
    
    except requests.exceptions.RequestException as e:
        # Handle issues like connection errors, timeouts, etc.
        print(f"Error fetching data from the API: {e}")
        return create_empty_dataframe()  
    
    except ValueError as e:
        print(f"Error decoding JSON: {e}")
        return create_empty_dataframe()
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return create_empty_dataframe()

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
        df['time'] = df.get('time', '').astype(str)
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
