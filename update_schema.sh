python3 \
    -m sgqlc.introspection \
    --exclude-deprecated \
    --exclude-description \
    http://localhost:9707/graphql \
    headquarters_schema.json

sgqlc-codegen schema headquarters_schema.json ssaw/headquarters_schema.py