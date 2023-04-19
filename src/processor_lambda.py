import os
import json
import awswrangler as wr
from datetime import datetime
from aws_lambda_powertools import Logger

logger = Logger()

ATHENA_RAW_DATABASE_NAME = os.getenv('ATHENA_RAW_DATABASE_NAME')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@logger.inject_lambda_context
def lambda_handler(event, context):
    # sample event in events/processor/country.json
    logger.info({"action":"invoke_lambda", "payload":{"event":event}})
    json_body = json.loads(event["Records"][0]["body"])
    state_event = json_body.get("state")
    index_event = json_body.get("index")

    # Extract data from Athena
    # - Query data to the specific state
    query = f"""
        select *
            , '{datetime_now}' as processed_time
            , {index_event} as index
        from covid_nytimes_states
        where state = '{state_event}'
    """
    logger.info({"action":"fetch_data", "payload":{"query":query, "db":ATHENA_RAW_DATABASE_NAME}})
    errors = []
    try:
        state_data = wr.athena.read_sql_query(query, database=ATHENA_RAW_DATABASE_NAME)
    except Exception as exception:
        errors.append(exception)
        logger.error({"action":"fetch_data", "payload":{"error":str(exception), "query":query, "db":ATHENA_RAW_DATABASE_NAME}})
    # Create your own transformations
    # Load data in s3
    wr.s3.to_parquet(df=state_data, path=f"s3://{S3_BUCKET_NAME}/index={index_event}/data.parquet")

    # Update the status item in Dynamo

    return {
        "statusCode": 200 if not errors else 400,
        "status": "success" if not errors else "error"
        }
