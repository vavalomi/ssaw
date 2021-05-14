#!/bin/bash

. ./env_vars.sh
if test -f "./env_vars_override.sh"; then
   . ./env_vars_override.sh
fi

docker rm $container_name --force
docker volume rm ${container_name}_app --force
docker volume rm ${container_name}_app_key --force
docker exec db dropdb -U postgres --if-exists $container_name

rm headquarters/vcr_cassettes/**
