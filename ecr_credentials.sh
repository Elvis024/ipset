#!/usr/bin/env bash

mkdir -p ~/.aws

cat > ~/.aws/credentials << EOL
[default]
aws_access_key_id=AKIAQBHSRDAZUQWGM7WA
aws_secret_access_key=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
EOL

cat > ~/.aws/config << EOL
[default]
region=us-east-1
output=json
EOL

