# Berlin-Weather-Project

data: https://www.kaggle.com/datasets/mexwell/berlin-hourly-weather-data?select=berlin_soil_temperature.csv

to download from Kaggle: https://www.youtube.com/watch?v=BlTvuNgTHR4&ab_channel=IndomitableTech


## Steps

TODOS: Containerize all

1. Create the repository (Git):
    - `git init`
    - `git remote add origin https://github.com/batxes/Berlin-Weather-Project.git`
    - `git branch -M main`

2. Python virtual environment (Pipenv):
    - Create requirements.txt, add some libraries (we will update this on the go)
    - `pipenv install -r requirements.txt`
    - `pipenv shell`

3. Infrastructure as Code (IaC) (Terraform):
    Here we will define and provision cloud resources. It is imporatnt for automation of infrastructure setup, reproducibility and scalability.
    - Install Terraform: https://developer.hashicorp.com/terraform/install?product_intent=terraform
    - Add google as provider and a GS bucket and Bigquery as resources
    - Add also a variables.tf so main.tf can be cleaner.
    - Now, We want to set up terraform in GCP. For that we need a service account. Go to Google Cloud and do the next steps:
        - Create a new project. Note the project ID into the variables 
        - Go to IAM and ADmin -> Service accounts -> Create service account (berlin-weather-service-account) -> Add roles (storage admin, bigquery admin, Compute ADmin). If in the future we want more roles or edit them, we can do that in IAM->edit-> roles
        - Create a new key (json) and save it in the computer. Edit the gitignore
        - terraform init. If sucessful it will create .terraform folder and .terraform.lock
        - I also added the .files from terraform to the gitignore, just in case
        - Now create a bucket. berlin-weather-bucket. Add to the main.tf as resource.
        - terraform plan -> terraform apply.
        - previous command gave error: Error: googleapi: Error 409: Your previous request to create the named bucket succeeded and you already own it., conflict 
        -  to fix, I used import: terraform import google_storage_bucket.data_lake berlin-weather-bucket
        - This happened because I created the bucket from the GCP web. With terraform, it could have been created directly. I will do this now for the bigquery dataset.
        - lets destroy what we have: terraform destroy. See that the bucket dissapears from the google cloud Platform.
        - adter adding the bigquery as resource, terraform plan, apply and check that it appears in GCP
        
4. Data Ingestion and Orchestration (Airflow/Prefect): Now we want to create a workflow (direct acyclic graph (DAG)) to ingest data (APIs, databases), upload to a data lake (GCS, S3) and load the data into the warehouse (Bigquery, Redshift). It is important to automate data ingestion and loading, reliability and scalability.
    - export AIRFLOW_HOME=~/work/Berlin-Weather-Project  NOTE: there has to be a way to add this which is not in the bashrc
    - `pip install apache-airflow` -> add also to requirements
    - `airflow db init`
    - `airflow users create --username admin --firstname Ibai --lastname Irastorza --role Admin --email batxes@gmail.com`
    -  add password (ninja)
    - `airflow webserver --port 8080` -> if this fails: pip install --upgrade apache-airflow
    - `airflow scheduler`
    - Access the Airflow UI at http://localhost:8080
    
    4.1  Now that we have airflow up and running, lets create a DAG for Data Ingestion

    - Create data_ingestion_dag.py in the dags/ directory
    - add google.cloud to requirements.txt. Install it before with pip install google.cloud
    - install and add also pip install --upgrade google-cloud-storage
    - Get the KAggle API. Put the json in ~/.kaggle and then I create a variables.py file where I pasted the username and key
    - add the variables.py to gitignore, we dont want our key there.
    - pip install kaggle
    - to check the name of the datasets: ╰─❯ kaggle datasets list -s berlin                                                                                
    - Note: if the dag fails because of GCP credentials, this worked: export GOOGLE_APPLICATION_CREDENTIALS="/home/ibai/work/Berlin-Weather-Project/keys/berlin-weather-project-25fec91b5442.json"
    - Note: Maybe we need to specify these exports beforehand
    - Added 2 more dags, to create a table and to load into bigquery
    - I need to install this also: pip install apache-airflow-providers-google  -> add to requirements.txt   
    - I added the OS.environ GCS credentials to the beginning of the code, because each task needs them


    - Meanwhile, I thought of creating a docker-compose with airflow so I can run it and forget about all steps in point 4. I downloaded the docker compose code from the official website. I added some variables so it can read my environment variables. Added also kaggle to requirements.
    

