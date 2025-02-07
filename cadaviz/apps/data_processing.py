import pandas as pd
import requests
import datetime

# API Endpoint
URL = "http://cadaviz_web:5000/ai/analytics/data"

def fetch_data():
    """Fetch data from API and return a cleaned DataFrame."""
    try:
        response = requests.get(URL)
        response.raise_for_status()  # Will raise an HTTPError if status_code is not 200
        
        data = response.json()  # Assuming data is a JSON list of records

        return process_json_data(data)
    
    except requests.exceptions.RequestException as e:
        # Handle issues like connection errors, timeouts, etc.
        print(f"Error fetching data from the API: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error
    
    except ValueError as e:
        # Handle errors related to JSON decoding if response is not valid JSON
        print(f"Error decoding JSON: {e}")
        return pd.DataFrame()
    
    except Exception as e:
        # Catch any other unforeseen exceptions
        print(f"An unexpected error occurred: {e}")
        return pd.DataFrame()

def process_json_data(data):
    """Convert JSON response to a cleaned Pandas DataFrame."""
    try:
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
    
    except Exception as e:
        # Catch any issues in the data processing step
        print(f"Error processing data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

# Get the current month start and end date
today = datetime.date.today()
start_of_month = today.replace(day=1)
end_of_month = today.replace(day=28) + pd.DateOffset(days=4)  # Moves to last day of month
end_of_month = end_of_month - pd.DateOffset(days=end_of_month.day)

# Default visualization selection
DEFAULT_VISUALIZATIONS = ['table', 'active-users']