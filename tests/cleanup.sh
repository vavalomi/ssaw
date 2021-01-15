#!/bin/bash

. ./env_vars.sh
if test -f "./env_vars_override.sh"; then
   . ./env_vars_override.sh
fi

docker rm $container_name --force
docker volume rm ssaw_testing_app --force
docker volume rm ssaw_testing_app_key --force
docker exec db dropdb -U postgres --if-exists $container_name

rm headquarters/vcr_cassettes/**
