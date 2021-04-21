#!/usr/bin/env bash

mkdir -p ~/.aws

cat > ~/.aws/credentials << EOL
[default]
aws_access_key_id=AKIAQBHSRDAZ6MZFOXNJ
aws_secret_access_key=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
EOL

cat > ~/.aws/config << EOL
[default]
region=us-east-1
output=json
EOL

