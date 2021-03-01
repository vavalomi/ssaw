#!/bin/bash

. ./env_vars.sh

if test -f "./env_vars_override.sh"; then
   . ./env_vars_override.sh
fi

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
