import os
import time
from aws_lambda_powertools import Logger

logger = Logger()

@logger.inject_lambda_context
def lambda_handler(event, context):
    logger.info({"action":"invoke_lambda", "payload":{"event":event}})

    finished_sg_ids = []
    for record in event["Records"]:
        event_name = record["eventName"]
        new_image = record["dynamodb"]['NewImage']
        finished_processes = new_image["finished_processes"]["N"]
        total_processes = new_image["total_processes"]["N"]
        
        if finished_processes == total_processes:
            finished_sg_ids.append(new_image["scatter_gather_id"]['S'])

    # report ScatterGather finished or trigger your next step
    for scatter_gather_id in finished_sg_ids:
        logger.info({"action":"finished_scatter_gather_id", "payload":{"scatter_gather_id":scatter_gather_id}})
