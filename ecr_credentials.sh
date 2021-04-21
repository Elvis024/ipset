#!/usr/bin/env bash

mkdir -p ~/.aws

cat > ~/.aws/credentials << EOL
[default]
aws_access_key_id=AKIAQBHSRDAZ2OZG6ENE
aws_secret_access_key=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
EOL

cat > ~/.aws/config << EOL
[default]
region=us-east-1
output=json
EOL
