#FROM apache/airflow:2.8.1-python3.12.3
FROM apache/airflow:3.0.0rc3-python3.12

COPY --chown=airflow:root requirements.txt /requirements.txt

USER airflow
RUN pip install --no-cache-dir -r /requirements.txt