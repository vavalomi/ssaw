#!/bin/bash

. ./env_vars.sh
if test -f "./env_vars_override.sh"; then
   . ./env_vars_override.sh
fi

sh ./cleanup.sh

sh ./create_instance.sh

$python populate_data.py
