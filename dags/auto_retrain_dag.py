from __future__ import annotations

import os
import requests
from datetime import datetime, timedelta

from airflow.decorators import dag, task

# Set this to the actual host and port of your application (possibly from ENV)
APP_HOST = os.getenv("APP_HOST", "http://localhost:5001")
RETRAIN_ENDPOINT = f"{APP_HOST}/auto_retrain_if_drifted"

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    dag_id="auto_retrain_model_dag",
    default_args=default_args,
    schedule_interval="*/45 * * * *",  # Every 45. minute for the demo's sake
    start_date=datetime(2025, 7, 30),
    catchup=False,
    tags=["ml", "retraining"]
)
def auto_retrain_model():

    @task(retries=0)
    def post_csv_to_retrain():
        csv_path = os.getenv("RETRAIN_CSV_PATH", "/opt/airflow/titanic_train500.csv")
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        with open(csv_path, "rb") as f:
            files = {"file": (os.path.basename(csv_path), f)}
            response = requests.post(RETRAIN_ENDPOINT, files=files)

        if response.status_code != 200:
            raise Exception(f"Request failed: {response.status_code} - {response.text}")

        result = response.json()
        print("Retraining result:", result)
        return result

    post_csv_to_retrain()

# Register the DAG
dag = auto_retrain_model()