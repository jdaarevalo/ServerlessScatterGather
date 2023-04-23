# ServerlessScatterGather


## Introduction

This repository contains the code and resources to implement the AWS Serverless Scatter-Gather Pattern, a powerful approach for optimizing data processing, enhancing performance, and streamlining resource usage in your data engineering projects.

Read the explanation and full details here https://aws.plainenglish.io/scalable-data-processing-with-aws-serverless-scatter-gather-pattern-implementation-63d25d6f6d23

## Architecture
![ServerlessScatterGather](https://user-images.githubusercontent.com/2475570/233821558-c15b9a69-8d1d-42aa-8923-737af54c5056.png)

## Features

- Getting data from Registry of Open Data on AWS
- Data processing using a AWS Lambda function (src/processar_lambda.py)
- Parallel execution through SQS and Lambda configuration
- DynamoDB Tables and Streams
- DynamoDB Streams as Lambda event 
- Integration with AWS services
- Scatter Gather Lambda functions

## Prerequisites

- AWS Account with necessary permissions to deploy SAM applications
- AWS CLI installed and configured
- Familiarity with AWS Lambda, DynamoDB AWS services

## Setup

1. Clone this repository: `git clone git@github.com:jdaarevalo/ServerlessScatterGather.git`
2. Update permissions execution to `deploy.sh`
3. Deploy the AWS resources with `./deploy.sh`

## Usage

Once deployed, you can test the scatter-gather pattern using the provided test event or by integrating it into your own data processing pipeline.

## Contributing

Please feel free to open an issue or submit a pull request if you'd like to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
