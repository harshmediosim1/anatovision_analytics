import pandas as pd
from apps.models import AnalyticsData
from apps.dashboard.logger import logger

def create_empty_dataframe():
    columns = ["id", "user_id", "version", "date", "time", "location", "college", "module", "submodule", "duration"]
    return pd.DataFrame(columns=columns)

def process_json_data(data):
    try:
        if not data:
            return create_empty_dataframe() 
        
        df = pd.DataFrame(data)

        required_columns = ["id", "user_id", "version", "date", "time", "location", "college", "module", "submodule", "duration"]
        for col in required_columns:
            if col not in df.columns:
                df[col] = "Unknown" if col not in ["date", "duration", "id"] else None

        df["id"] = pd.to_numeric(df["id"], errors="coerce")  # Ensure ID is numeric

        return df
    
    except Exception as e:
        logger.error(f"Error processing data: {e}", exc_info=True)
        return create_empty_dataframe()

def fetch_data():
    try:
        records = AnalyticsData.query.order_by(AnalyticsData.date.desc()).all()
        if not records:
            return create_empty_dataframe(), None
        
        result = [
            {
                "id": r.id,
                "version": r.version,
                "user_id": r.user_id,
                "college": r.college,
                "location": r.location,
                "date": r.date.isoformat(),
                "module": r.module,
                "submodule": r.submodule,
                "time": r.time,
                "duration": r.duration
            }
            for r in records
        ]

        df = process_json_data(result)
        return df, None
    except Exception as e:
        logger.error(f"Error fetching data from DB: {e}", exc_info=True)
        return create_empty_dataframe(), None

DEFAULT_VISUALIZATIONS = ['table', 'active-users']
