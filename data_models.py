from enum import Enum
from typing import List
from pydantic import BaseModel


class ModelLanguage(str, Enum):
    fr = 'fr'
    en = 'en'


class ModelSize(str, Enum):
    sm = 'sm'
    md = 'md'
    lg = 'lg'


class UserRequestIn(BaseModel):
    text: str
    model_language: ModelLanguage = 'en'
    model_size: ModelSize = 'sm'


class EntityOut(BaseModel):
    start: int
    end: int
    type: str
    text: str


class EntitiesOut(BaseModel):
    entities: List[EntityOut]
    anonymized_text: str
