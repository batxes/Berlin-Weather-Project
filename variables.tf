variable "credentials" {
    description = "My Credentials"
    default = "./keys/berlin-weather-project-25fec91b5442.json"
}

variable "project" {
  description = "Project"
  default     = "berlin-weather-project"
}

variable "region" {
  description = "Region"
  default     = "europe-west3"
}

variable "location" {
  description = "Project Location"
  default     = "EU"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "berlin_weather_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "berlin-weather-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}

