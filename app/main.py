import boto3
import botocore
from dotenv import dotenv_values
from fastapi import FastAPI
from model import (CatalogTargets, DeltaTargets, ErrorResponse,
                   ExceptionResponse, JdbcTargets, S3Targets, SuccessResponse)

config = dotenv_values(".env")
ACCESS_ID = config.get("aws_access_key_id")
ACCESS_KEY = config.get("aws_secret_access_key")
REGION = config.get("aws_region")


client = boto3.client('glue', aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=ACCESS_KEY, region_name=REGION)

app = FastAPI(openapi_url="/crawler/openapi.json", docs_url="/crawler/docs")


@app.post("/crawler/create_s3_crawler")
async def create_s3_crawler(glue: S3Targets):
    """
    This endpoint creates a Glue crawler for S3 target.
    """
    try:
        response = client.create_crawler(
            Name=glue.Name,
            Role=glue.Role,
            DatabaseName=glue.DatabaseName,
            Targets={
                'S3Targets': [
                    {
                        'Path': glue.S3Path
                    },
                ]})
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return SuccessResponse(status=response['ResponseMetadata']['HTTPStatusCode'])
        else:
            return ErrorResponse(status=response['ResponseMetadata']['HTTPStatusCode'], data=response)
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'InvalidInputException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'AlreadyExistsException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'OperationTimeoutException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'ResourceNumberLimitExceededException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        else:
            return ExceptionResponse()
    except Exception as e:
        return ExceptionResponse()


@app.post("/crawler/create_jdbc_crawler")
async def create_jdbc_crawler(glue: JdbcTargets):
    """
    This endpoint creates a Glue crawler for JDBC target.
    """
    try:
        response = client.create_crawler(
            Name=glue.Name,
            Role=glue.Role,
            DatabaseName=glue.DatabaseName,
            Targets={
                'JdbcTargets': [
                    {
                        'ConnectionName': glue.ConnectionName,
                        'Path': glue.Path,
                    },
                ]})
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return SuccessResponse(status=response['ResponseMetadata']['HTTPStatusCode'])
        else:
            return ErrorResponse(status=response['ResponseMetadata']['HTTPStatusCode'], data=response)
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'InvalidInputException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'AlreadyExistsException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'OperationTimeoutException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'ResourceNumberLimitExceededException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        else:
            return ExceptionResponse()
    except Exception as e:
        return ExceptionResponse()


@app.post("/crawler/create_catalog_crawler")
async def create_catalog_crawler(glue: CatalogTargets):
    """
    This endpoint creates a Glue crawler for catalog target.
    """

    try:
        response = client.create_crawler(
            Name=glue.Name,
            Role=glue.Role,
            Targets={
                'CatalogTargets': [
                    {
                        'DatabaseName': glue.DatabaseName,
                        'Tables': [
                            glue.Tables,
                        ],
                    },
                ]},
            SchemaChangePolicy={
                'UpdateBehavior': glue.UpdateBehavior,
                'DeleteBehavior': glue.DeleteBehavior
            })
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return SuccessResponse(status=response['ResponseMetadata']['HTTPStatusCode'])
        else:
            return ErrorResponse(status=response['ResponseMetadata']['HTTPStatusCode'], data=response)
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'InvalidInputException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'AlreadyExistsException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'OperationTimeoutException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'ResourceNumberLimitExceededException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        else:
            return ExceptionResponse()
    except Exception as e:
        return ExceptionResponse()


@app.post("/crawler/create_delta_crawler")
async def create_delta_crawler(glue: DeltaTargets):
    """
    This endpoint creates a Glue crawler for delta target.
    """
    try:
        response = client.create_crawler(
            Name=glue.Name,
            Role=glue.Role,
            DatabaseName=glue.DatabaseName,
            Targets={
                'DeltaTargets': [
                    {
                        'DeltaTables': [
                            glue.DeltaTables,
                        ],
                    },
                ]})
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return SuccessResponse(status=response['ResponseMetadata']['HTTPStatusCode'])
        else:
            return ErrorResponse(status=response['ResponseMetadata']['HTTPStatusCode'], data=response)
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'InvalidInputException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'AlreadyExistsException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'OperationTimeoutException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'ResourceNumberLimitExceededException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        else:
            return ExceptionResponse()
    except Exception as e:
        return ExceptionResponse()


@app.get('/crawler/get_crawlers')
async def get_crawlers():
    """
    This endpoint return the all Glue crawler.
    The supported target types are: S3Targets, JdbcTargets, CatalogTargets, DeltaTargets.
    """
    try:
        response = client.get_crawlers()
        return SuccessResponse(status=response['ResponseMetadata']['HTTPStatusCode'], data=response)
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'OperationTimeoutException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        else:
            return ExceptionResponse()
    except Exception as e:
        return ExceptionResponse()


@app.get('/crawler/get_crawler/{crawler_name}')
async def get_crawler(crawler_name: str):
    """
    This endpoint return the Glue crawler based on param.
    The supported target types are: S3Targets, JdbcTargets, CatalogTargets, DeltaTargets.
    """
    try:
        response = client.get_crawler(
            Name=crawler_name
        )
        return SuccessResponse(status=response['ResponseMetadata']['HTTPStatusCode'], data=response)
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'EntityNotFoundException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'OperationTimeoutException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        else:
            return ExceptionResponse()
    except Exception as e:
        return ExceptionResponse()


@app.get('/crawler/list_crawlers')
async def list_crawlers():
    """
    This endpoint return the List of all Glue crawler.
    The supported target types are: S3Targets, JdbcTargets, CatalogTargets, DeltaTargets.
    """
    try:
        response = client.list_crawlers()
        return SuccessResponse(status=response['ResponseMetadata']['HTTPStatusCode'], data=response)
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'OperationTimeoutException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        else:
            return ExceptionResponse()
    except Exception as e:
        return ExceptionResponse()


@app.get('/crawler/start_crawler/{crawler_name}')
async def start_crawlers(crawler_name: str):
    """
    This endpoint run the Glue crawler based on param.
    The supported target types are: S3Targets, JdbcTargets, CatalogTargets, DeltaTargets.
    """
    try:
        response = client.start_crawler(Name=crawler_name)
        return SuccessResponse(status=response['ResponseMetadata']['HTTPStatusCode'], data={"message": "Crawler started successfully"})
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'EntityNotFoundException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'CrawlerRunningException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'OperationTimeoutException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        else:
            return ExceptionResponse()
    except Exception as e:
        return ExceptionResponse()


@app.get('/crawler/stop_crawler/{crawler_name}')
async def stop_crawlers(crawler_name: str):
    """
    This endpoint stop the Glue crawler based on param.
    The supported target types are: S3Targets, JdbcTargets, CatalogTargets, DeltaTargets.
    """
    try:
        response = client.stop_crawler(Name=crawler_name)
        print('res', response)
        return SuccessResponse(status=response['ResponseMetadata']['HTTPStatusCode'], data={"message": "Crawler stopped successfully"})
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'EntityNotFoundException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'CrawlerNotRunningException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'CrawlerStoppingException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'OperationTimeoutException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        else:
            return ExceptionResponse()
    except Exception as e:
        return ExceptionResponse()


@app.put("/crawler/update_s3_crawler")
async def update_s3_crawler(glue: S3Targets):
    """
    This endpoint update a Glue crawler for S3 target.
    """
    try:
        response = client.update_crawler(
            Name=glue.Name,
            Role=glue.Role,
            DatabaseName=glue.DatabaseName,
            Targets={
                'S3Targets': [
                    {
                        'Path': glue.S3Path
                    },
                ]})
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return SuccessResponse(status=response['ResponseMetadata']['HTTPStatusCode'], data=response)
        else:
            return ErrorResponse(status=response['ResponseMetadata']['HTTPStatusCode'], data=response)
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'InvalidInputException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'VersionMismatchException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'EntityNotFoundException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'CrawlerRunningException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'OperationTimeoutException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        else:
            return ExceptionResponse()
    except Exception as e:
        return ExceptionResponse()


@app.put("/crawler/update_jdbc_crawler")
async def update_jdbc_crawler(glue: JdbcTargets):
    """
    This endpoint update a Glue crawler for JDBC target.
    """

    try:
        response = client.update_crawler(
            Name=glue.Name,
            Role=glue.Role,
            DatabaseName=glue.DatabaseName,
            Targets={
                'JdbcTargets': [
                    {
                        'ConnectionName': glue.ConnectionName,
                        'Path': glue.Path,
                    },
                ]})
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return SuccessResponse(status=response['ResponseMetadata']['HTTPStatusCode'], data=response)
        else:
            return ErrorResponse(status=response['ResponseMetadata']['HTTPStatusCode'], data=response)
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'InvalidInputException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'VersionMismatchException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'EntityNotFoundException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'CrawlerRunningException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'OperationTimeoutException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        else:
            return ExceptionResponse()
    except Exception as e:
        return ExceptionResponse()


@app.put("/crawler/update_catalog_crawler")
async def update_catalog_crawler(glue: CatalogTargets):
    """
    This endpoint update a Glue crawler for catalog target.
    """

    try:
        response = client.update_crawler(
            Name=glue.Name,
            Role=glue.Role,
            Targets={
                'CatalogTargets': [
                    {
                        'DatabaseName': glue.DatabaseName,
                        'Tables': [
                            glue.Tables,
                        ],
                    },
                ]},
            SchemaChangePolicy={
                'UpdateBehavior': glue.UpdateBehavior,
                'DeleteBehavior': glue.DeleteBehavior
            })
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return SuccessResponse(status=response['ResponseMetadata']['HTTPStatusCode'], data=response)
        else:
            return ErrorResponse(status=response['ResponseMetadata']['HTTPStatusCode'], data=response)
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'InvalidInputException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'VersionMismatchException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'EntityNotFoundException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'CrawlerRunningException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'OperationTimeoutException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        else:
            return ExceptionResponse()
    except Exception as e:
        return ExceptionResponse()


@app.put("/crawler/update_delta_crawler")
async def update_delta_crawler(glue: DeltaTargets):
    """
    This endpoint update a Glue crawler for delta target.
    """
    try:
        response = client.update_crawler(
            Name=glue.Name,
            Role=glue.Role,
            DatabaseName=glue.DatabaseName,
            Targets={
                'DeltaTargets': [
                    {
                        'DeltaTables': [
                            glue.DeltaTables,
                        ],
                    },
                ]})
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return SuccessResponse(status=response['ResponseMetadata']['HTTPStatusCode'], data=response)
        else:
            return ErrorResponse(status=response['ResponseMetadata']['HTTPStatusCode'], data=response)
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'InvalidInputException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'VersionMismatchException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'EntityNotFoundException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'CrawlerRunningException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        if error.response['Error']['Code'] == 'OperationTimeoutException':
            return ExceptionResponse(status=error.response['ResponseMetadata']['HTTPStatusCode'], message=error.response['Error'])
        else:
            return ExceptionResponse()
    except Exception as e:
        return ExceptionResponse()
