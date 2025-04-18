from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyTableOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from google.cloud import storage
import os
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
# add previous directory where variables.py is
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import variables
import kaggle

# do it here so all tasks use it
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = variables.gcp_credentials

with DAG(
    dag_id="data_ingestion_dag",
    start_date=datetime(year=2025, month=1, day=1, hour=9, minute=0),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    render_template_as_native_obj=True
) as dag:

    def authenticate_in_kaggle():
        # setup as OS variables
        os.environ["KAGGLE_USERNAME"] = variables.kaggle_username
        os.environ["KAGGLE_KEY"] = variables.kaggle_key

        # import kaggle itself seems to be executing an authentication step and fails if kaggle credentials not found
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files(variables.kaggle_dataset, path=variables.kaggle_dataset_path, unzip=True)
        print ("Kaggle authentication successful")

        # create blob dir
        if not os.path.exists('raw'):
            os.makedirs('raw')
        print ("raw dir created")



    task1_authenticate = PythonOperator(
        dag=dag,
        task_id="Authenticate_in_Kaggle",
        python_callable=authenticate_in_kaggle
    )

    # Function to upload data to GCS
    def upload_to_gcs():
        client = storage.Client()
        bucket = client.bucket(variables.bucket_name)
        files = variables.kaggle_source_file_names
        for f in files:
            print (f)
            blob = bucket.blob(f)
            f_local = variables.kaggle_dataset_path+"/"+f
            blob.upload_from_filename(f_local)
            print(f"File {f_local} uploaded to {f}.")

    task2_ingest = PythonOperator(
        dag=dag,
        task_id="Ingest_data_from_Kaggle",
        python_callable=upload_to_gcs
    )
    
    # Task to create a BigQuery table
    task3_create_table_soil = BigQueryCreateEmptyTableOperator(
        task_id='create_bigquery_table_soil',
        dataset_id=variables.bq_dataset_name,
        table_id=variables.bq_table_id_soil,
        schema_fields=[
            {'name': 'STATIONS_ID', 'type': 'INTEGER', 'mode': 'REQUIRED'},
            {'name': 'MESS_DATUM', 'type': 'STRING', 'mode': 'REQUIRED'},  # Assuming timestamp format needs parsing
            {'name': 'QN_2', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'V_TE002', 'type': 'FLOAT', 'mode': 'NULLABLE'},
            {'name': 'V_TE005', 'type': 'FLOAT', 'mode': 'NULLABLE'},
            {'name': 'V_TE010', 'type': 'FLOAT', 'mode': 'NULLABLE'},
            {'name': 'V_TE020', 'type': 'FLOAT', 'mode': 'NULLABLE'},
            {'name': 'V_TE050', 'type': 'FLOAT', 'mode': 'NULLABLE'},
            {'name': 'V_TE100', 'type': 'FLOAT', 'mode': 'NULLABLE'},
            {'name': 'eor', 'type': 'STRING', 'mode': 'NULLABLE'},  # Seems like a marker, keeping as STRING
        ],
        #time_partitioning={
        #    'type': 'DAY',
        #    'field': 'transaction_date',
        #},
        #clustering_fields=['customer_id'],
        dag=dag,
    )

    # Task to load data into BigQuery
    task4_load_into_bq_soil = GCSToBigQueryOperator(
        task_id='load_data_to_bigquery_soil',
        bucket=variables.bucket_name,
        source_objects=["berlin_soil_temperature.csv"],
        destination_project_dataset_table=f'{variables.bq_dataset_name}.{variables.bq_table_id_soil}',
        schema_fields=[
            {'name': 'STATIONS_ID', 'type': 'INTEGER', 'mode': 'REQUIRED'},
            {'name': 'MESS_DATUM', 'type': 'STRING', 'mode': 'REQUIRED'},  # Assuming timestamp format needs parsing
            {'name': 'QN_2', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'V_TE002', 'type': 'FLOAT', 'mode': 'NULLABLE'},
            {'name': 'V_TE005', 'type': 'FLOAT', 'mode': 'NULLABLE'},
            {'name': 'V_TE010', 'type': 'FLOAT', 'mode': 'NULLABLE'},
            {'name': 'V_TE020', 'type': 'FLOAT', 'mode': 'NULLABLE'},
            {'name': 'V_TE050', 'type': 'FLOAT', 'mode': 'NULLABLE'},
            {'name': 'V_TE100', 'type': 'FLOAT', 'mode': 'NULLABLE'},
            {'name': 'eor', 'type': 'STRING', 'mode': 'NULLABLE'},  # Seems like a marker, keeping as STRING
        ],
        write_disposition='WRITE_TRUNCATE',
        skip_leading_rows=1,  # Skip header row
        field_delimiter=';',  # Adjust if necessary
        max_bad_records=10, # remove the row containing column names again
        dag=dag,
    )

    # Define task dependencies
    task1_authenticate >> task2_ingest >> task3_create_table_soil >> task4_load_into_bq_soil
    #(task1_authenticate >> task2_ingest >> [task3_create_table_soil, task3_create_table_wind])
    #(task3_create_table_soil >> task4_load_into_bq_soil)
    #(task3_create_table_wind >> task4_load_into_bq_wind)

if __name__ == '__main__':
    authenticate_in_kaggle()
    upload_to_gcs()


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

