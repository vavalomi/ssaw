python3 \
    -m sgqlc.introspection \
    --exclude-deprecated \
    --exclude-description \
    https://hqrc.mysurvey.solutions/graphql \
    headquarters_schema.json

sgqlc-codegen schema headquarters_schema.json ssaw/headquarters_schema.py