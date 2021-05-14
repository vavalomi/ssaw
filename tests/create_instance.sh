#!/bin/bash

. ./env_vars.sh

if test -f "./env_vars_override.sh"; then
   . ./env_vars_override.sh
fi

docker volume create ${container_name}_app
docker volume create ${container_name}_app_key

. ./start_instance.sh

 until docker exec $container_name /app/WB.UI.Headquarters manage users create \
   --role Administrator --login=$admin_username --password=$admin_password > /dev/null 2>&1; do sleep 2; done

docker exec $container_name /app/WB.UI.Headquarters manage users create \
   --role ApiUser --login=$SOLUTIONS_API_USER --password=$SOLUTIONS_API_PASSWORD --workspace=primary
