#!/bin/bash

# To deploy it manually

# $chmod +x deploy.sh
# $./deploy.sh staging

# Variables
export AWS_REGION=eu-west-1
export ENVIRONMENT="staging"
export AWS_PROFILE="default"
export STACK_NAME="serverless-scatter-gather"


sam build
sam deploy \
--profile=${AWS_PROFILE} \
--stack-name "${STACK_NAME}" \
--region "${AWS_REGION}" \
--resolve-s3 \
--parameter-overrides Environment=${ENVIRONMENT} \
--capabilities CAPABILITY_NAMED_IAM
