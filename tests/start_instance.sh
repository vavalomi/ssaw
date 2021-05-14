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
    --env HQ_Captcha__CaptchaType="Recaptcha" \
    --env HQ_Captcha__SecretKey="$captcha_secretkey" \
    --env HQ_Captcha__SiteKey="$captcha_sitekey" \
    --env HQ_Captcha__Version="v2" \
    --publish "$expose_port:80" \
    --volume "${container_name}_app:/app/AppData" \
    --volume "${container_name}_app_key:/root/.aspnet/DataProtection-Keys" \
    $image_name
