import boto3
from datetime import datetime
from aws_lambda_powertools import Logger

logger = Logger()
dynamodb = boto3.resource('dynamodb')
status_finished = "finished"

def create_item(table_name, item):
    logger.info({"action":"create_dynamo_item", "payload":{"table_name":table_name, "item":item}})
    table = dynamodb.Table(table_name)
    datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item["created_at"] = datetime_now
    item["updated_at"] = datetime_now
    try:
        table.put_item(Item=item)
        logger.info({"action":"created_dynamo_item", "payload":{"item":item}})
    except Exception as exception:
        logger.error({"action":"created_dynamo_item", "payload":{"exception":exception, "table_name":table_name, "item":item}})

def update_item_finished(table_name, item):
    logger.info({"action":"update_dynamo_item", "payload":{"table_name":table_name, "item":item}})
    table = dynamodb.Table(table_name)
    datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        table.update_item(
            Key={
                'scatter_gather_id': item["scatter_gather_id"],
                'process_id': item["process_id"]
            },
            UpdateExpression='SET #status = :status, #updated_at = :updated_at',
            ExpressionAttributeNames={
                '#status': 'status',
                '#updated_at': 'updated_at'
            },
            ExpressionAttributeValues={
                ':status': status_finished,
                ':updated_at': datetime_now
            }
        )
        logger.info({"action":"updated_dynamo_item", "payload":{"item":item}})
    except Exception as exception:
        logger.error({"action":"updated_dynamo_item", "payload":{"exception":exception, "table_name":table_name, "item":item}})

def update_finished_processes(table_name, scatter_gather_id, value_to_sum):
    logger.info({"action":"update_finished_processes", "payload":{"table_name":table_name, "scatter_gather_id":scatter_gather_id, "value":value_to_sum}})
    table = dynamodb.Table(table_name)
    datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        table.update_item(
            Key={
                'scatter_gather_id': scatter_gather_id
            },
            UpdateExpression='SET finished_processes = finished_processes + :val, #updated_at = :updated_at',
            ExpressionAttributeValues={
                ':val': value_to_sum,
                ':updated_at': datetime_now
            },
            ExpressionAttributeNames={
                '#updated_at': 'updated_at'
            },
            ReturnValues='ALL_NEW'
        )
        logger.info({"action":"updated_finished_processes", "payload":{"scatter_gather_id":scatter_gather_id, "value":value_to_sum}})
    except Exception as exception:
        logger.error({"action":"updated_finished_processes", "payload":{"exception":exception, "table_name":table_name, "scatter_gather_id":scatter_gather_id, "value":value_to_sum}})
