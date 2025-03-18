# Berlin-Weather-Project


## Steps

1. Create the repository:
    - git init
    - git remote add origin https://github.com/batxes/Berlin-Weather-Project.git
    - git branch -M main

2. Python virtual environment:
    - Create requirements.txt, add some libraries (we will update this on the go)
    - pipenv install -r requirements.txt
    - pipenv shell

3. Infrastructure as Code (IaC):
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
        - 

