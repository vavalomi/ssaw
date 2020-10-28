python.exe^
    -m sgqlc.introspection^
    --exclude-deprecated^
    --exclude-description^
    https://demo.mysurvey.solutions/graphql^
    headquarters_schema.json

python.exe sgqlc-codegen headquarters_schema.json ssaw\headquarters_schema.py