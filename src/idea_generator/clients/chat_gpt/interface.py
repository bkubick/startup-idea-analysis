# coding: utf-8
import enum
import typing

from pydantic import BaseModel, field_validator


class GPTModel(enum.Enum):
    GPT_35_TURBO = "gpt-3.5-turbo"
    GPT_35_TURBO_16K = "gpt-3.5-turbo-16k"
    GPT_4 = "gpt-4"


class Message(BaseModel):
    role: str
    content: str


class GPTRequestData(BaseModel):
    model: GPTModel
    messages: typing.List[Message]
    temperature: float

    class Config:
       json_encoders = {
              GPTModel: lambda v: v.value
         }
    
    @field_validator("temperature")
    def check_temperature(cls, values):
        if values < 0 or values > 1:
            raise ValueError("Temperature must be between 0 and 1")


class GPTResponseChoice(BaseModel):
    finish_reason: str
    index: int
    message: Message


class GPTResponseData(BaseModel):
    choices: typing.List[GPTResponseChoice]
    created: int
    id: str
    model: str
    object: str
