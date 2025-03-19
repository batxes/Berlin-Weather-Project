from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from google.cloud import storage
import os
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
# add previous directory where variables.py is
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import variables

with DAG(
    dag_id="data_ingestion_dag",
    start_date=datetime(year=2025, month=1, day=1, hour=9, minute=0),
    schedule="@daily",
    catchup=True,
    max_active_runs=1,
    render_template_as_native_obj=True
) as dag:

    def authenticate_in_kaggle():
        # setup as OS variables
        os.environ["KAGGLE_USERNAME"] = variables.kaggle_username
        os.environ["KAGGLE_KEY"] = variables.kaggle_key
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = variables.gcp_credentials
        print (os.environ)

        # import kaggle itself seems to be executing an authentication step and fails if kaggle credentials not found
        import kaggle
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files(variables.kaggle_dataset, path=variables.kaggle_dataset_path, unzip=True)

        # create blob dir
        if not os.path.exists('raw'):
            os.makedirs('raw')
        print ("Kaggle authentication successful")



    task1_authenticate = PythonOperator(
        dag=dag,
        task_id="Authenticate_in_Kaggle",
        python_callable=authenticate_in_kaggle
    )

    # Function to upload data to GCS
    def upload_to_gcs():
        client = storage.Client()
        bucket = client.bucket(variables.bucket_name)
        blob = bucket.blob(variables.destination_blob_name)
        blob.upload_from_filename(variables.kaggle_source_file_name)
        print(f"File {variables.kaggle_source_file_name} uploaded to {variables.destination_blob_name}.")

    task2_ingest = PythonOperator(
        dag=dag,
        task_id="Ingest_data_from_Kaggle",
        python_callable=upload_to_gcs
    )

    task1_authenticate >> task2_ingest

## Define the DAG
#default_args = {
#    'owner': 'airflow',
#    'start_date': datetime(2025, 01, 01),
#    'depends_on_past': False,
#    'email': ['batxes@gmail.com'],
#    'email_on_failure': False,
#    'email_on_retry': False,
#    'retries': 0,
#    'retry_delay': timedelta(minutes=20),
#    'execution_timeout' : timedelta(minutes=10),
#}

    #dag = DAG(
    #    dag_id='data_ingestion_dag',
    #    default_args=default_args,
    #    description='A DAG to ingest Kaggle data into GCS',
    #    schedule_interval='@daily',
    #    catchup=False
    #)

