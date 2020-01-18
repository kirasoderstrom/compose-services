#!/bin/bash
# Script to create and re-create es indices and setup guppy

sleep 2
docker exec esproxy-service curl -X DELETE $ELASTICSEARCH_URL/etl_0 --insecure
sleep 2
docker exec esproxy-service curl -X DELETE $ELASTICSEARCH_URL/file_0 --insecure
sleep 2
docker exec esproxy-service curl -X DELETE $ELASTICSEARCH_URL/file-array-config_0 --insecure
sleep 2
docker exec esproxy-service curl -X DELETE $ELASTICSEARCH_URL/etl-array-config_0 --insecure
sleep 2
docker exec tube-service bash -c "python run_config.py && python run_etl.py"

docker container stop guppy-service
docker container start guppy-service
