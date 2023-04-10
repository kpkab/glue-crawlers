from typing import Optional, Union

from pydantic import BaseModel, Field


class Glue_crawler(BaseModel):
    Name: str = Field(min_length=1, max_length=255)
    Role: str
    DatabaseName: str


class S3Targets(Glue_crawler):
    S3Path: str


class JdbcTargets(Glue_crawler):
    ConnectionName: str
    Path: str


class CatalogTargets(Glue_crawler):
    Tables: str
    UpdateBehavior: Optional[str] = "LOG"
    DeleteBehavior: Optional[str] = "LOG"


class DeltaTargets(Glue_crawler):
    DeltaTables: str


class SuccessResponse(BaseModel):
    success: bool = True
    status: int = 200
    data: Union[None, dict, list] = None


class ErrorResponse(BaseModel):
    success: bool = False
    status: int = 404
    message: Union[None, dict, list] = {"message": "Something wrong"}


class ExceptionResponse(BaseModel):
    success: bool = False
    status: int = 404
    message: Union[None, dict, list] = {"message": "Unhandled Exception"}
