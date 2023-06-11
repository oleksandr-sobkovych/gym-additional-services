from pydantic import BaseModel, Field, EmailStr, PositiveInt
from datetime import datetime
from typing import List, Union, Optional
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class ServiceType(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    type_name: str = Field(...)
    type_descr: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ServiceProvider(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    provider_name: str = Field(...)
    email: EmailStr = Field(...)
    provider_descr: str = Field(...)
    types: List[ServiceType] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Service(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    type: ServiceType = Field(...)
    provider_id: PyObjectId = Field(...)
    start: datetime = Field(...)
    end: datetime = Field(...)
    price: PositiveInt = Field(...)
    booked_by: Optional[Union[str, List[str]]]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Client(BaseModel):
    id: str = Field(..., alias="_id")
    booked_services: List[PyObjectId] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class Invoice(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    price: PositiveInt = Field(...)
    verified: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
