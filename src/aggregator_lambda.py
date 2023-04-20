import os
import time
from aws_lambda_powertools import Logger
from dynamo_operations import update_finished_processes

logger = Logger()
timestamp = int(time.time())

SG_AGGREGATE_TABLE_NAME = os.getenv('SG_AGGREGATE_TABLE_NAME')

@logger.inject_lambda_context
def lambda_handler(event, context):
    logger.info({"action":"invoke_lambda", "payload":{"event":event}})

    agg_scatter_gather_id = {}
    for record in event["Records"]:
        new_image = record["dynamodb"]['NewImage']
        status = new_image["status"]['S']
        scatter_gather_id = new_image["scatter_gather_id"]['S']
        
        if status == "finished":
            agg_scatter_gather_id[scatter_gather_id] = agg_scatter_gather_id.get(scatter_gather_id, 0) + 1

    logger.info({"action":"agg_scatter_gather_id", "payload":{"agg_scatter_gather_id":agg_scatter_gather_id}})

    # update total_finished values in dynamo for each scatter_gather_id
    for scatter_gather_id, value_to_sum in agg_scatter_gather_id.items():
        update_finished_processes(SG_AGGREGATE_TABLE_NAME, scatter_gather_id, value_to_sum)

    return { 
        "statusCode": 200, 
        "status": "success"
        }
