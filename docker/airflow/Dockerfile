ARG AIRFLOW_IMAGE_TAG=3.2.1-python3.12
FROM apache/airflow:${AIRFLOW_IMAGE_TAG}

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends vim less procps && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* \

USER airflow
WORKDIR /opt/airflow