import os
import boto3
import json
import time
import awswrangler as wr
from aws_lambda_powertools import Logger
from dynamo_operations import create_item

logger = Logger()

ATHENA_RAW_DATABASE_NAME = os.getenv('ATHENA_RAW_DATABASE_NAME')
QUEUE_URL = os.getenv('QUEUE_URL')
SG_PROCESSSES_TABLE_NAME = os.getenv('SG_PROCESSES_TABLE_NAME')
SG_AGGREGATE_TABLE_NAME = os.getenv('SG_AGGREGATE_TABLE_NAME')

@logger.inject_lambda_context
def lambda_handler(event, context):
    logger.info({"action":"invoke_lambda", "payload":{"event":event}})
    timestamp = int(time.time())
    # read the contries from the athena table
    query = "select distinct state from covid_nytimes_states"
    unique_states = wr.athena.read_sql_query(query, database=ATHENA_RAW_DATABASE_NAME)
    
    # write in SG_AGGREGATE_TABLE_NAME DynamoDB table how many states should be executed
    item = {
        "scatter_gather_id" : str(timestamp),
        "total_processes": len(unique_states),
        "finished_processes": 0
    }
    create_item(SG_AGGREGATE_TABLE_NAME, item)

    # For each state send the message queue
    # We want to Trigger processor_lambda by state
    for index, row in unique_states.iterrows():
        state = row['state']

        #store dynamo data by processes triggered
        item_state = {
            "scatter_gather_id" : str(timestamp),
            "process_id" : "{}_{}".format(index, state),
            "status": "started"
        }
        create_item(SG_PROCESSSES_TABLE_NAME, item_state)

        formatted_message = '{{"state":"{}", "index":{}, "item_state":{}}}'.format(
            state, index, json.dumps(item_state))

        logger.info({"action":"message_queue", "payload":{"message":formatted_message}})
        send_message_queue(formatted_message)
 
    return { 
        "statusCode": 200, 
        "status": "success",
        "data": {"states": len(unique_states)}
        }

def send_message_queue(message):
    sqs_client =boto3.client("sqs")
    response = sqs_client.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=str(message)
    )
    logger.info({"action":"send_message_queue", "payload":{"message":message,"response":response}})