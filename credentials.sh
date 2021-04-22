#!/usr/bin/env bash

mkdir -p ~/.aws



cat > ~/.aws/config << EOL
[default]
region=us-east-1
output=json
EOL
