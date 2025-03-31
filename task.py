from celery import Celery
import pandas as pd
import json

# Celery App Setup (Redis as Broker & Backend)
celery_app = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")

@celery_app.task
def process_json_task(locations_json, metadata_json):
    try:
        # Load JSON data
        locations_data = json.loads(locations_json)
        metadata_data = json.loads(metadata_json)

        # Convert to Pandas DataFrame
        df_locations = pd.DataFrame(locations_data)
        df_metadata = pd.DataFrame(metadata_data)

        # Merge Data on 'id'
        df = pd.merge(df_locations, df_metadata, on="id", how="left")

        # Count Locations Per Type
        location_counts = df["type"].value_counts().to_dict()

        # Average Rating Per Type
        avg_ratings = df.groupby("type")["rating"].mean().to_dict()

        # Most Reviewed Location
        most_reviewed = df.loc[df["reviews"].idxmax()].to_dict()

        # Identify Incomplete Data
        missing_data = df[df.isnull().any(axis=1)].to_dict(orient="records")

        # Return Processed Data
        return {
            "location_counts": location_counts,
            "avg_ratings": avg_ratings,
            "most_reviewed": most_reviewed,
            "missing_data": missing_data
        }
    except Exception as e:
        return {"error": str(e)}
