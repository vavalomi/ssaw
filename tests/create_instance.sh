#!/bin/bash

. ./env_vars.sh

if test -f "./env_vars_override.sh"; then
   . ./env_vars_override.sh
fi

docker volume create ssaw_testing_app
docker volume create ssaw_testing_app_key

docker run -d --rm \
    --name $container_name \
    --network "db-net" \
    --env ASPNETCORE_ENVIRONMENT="Production" \
    --env HQ_ConnectionStrings__DefaultConnection="$conn_string" \
    --env HQ_Headquarters__BaseUrl="$base_url" \
    --env HQ_Headquarters__TenantName="default" \
    --env Export_ExportSettings__DirectoryPath="/app/AppData/Export" \
    --env HQ_Logging__LogsLocation="/app/AppData/logs" \
    --publish "$expose_port:80" \
    --volume "ssaw_testing_app:/app/AppData" \
    --volume "ssaw_testing_app_key:/root/.aspnet/DataProtection-Keys" \
    surveysolutions/surveysolutions

 until docker exec $container_name /app/WB.UI.Headquarters manage users create \
   --role Administrator --login=$admin_username --password=$admin_password > /dev/null 2>&1; do sleep 2; done

docker exec $container_name /app/WB.UI.Headquarters manage users create \
   --role ApiUser --login=$SOLUTIONS_API_USER --password=$SOLUTIONS_API_PASSWORD
