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
    selected_entities: List[str]


class EntityOut(BaseModel):
    text: str
    anonymized_text: str = ''
    common_name: str = ''
    entity_type: str
    start_idx:  int


class EntitiesOut(BaseModel):
    tokens: List[EntityOut]
    anonymized_text: str
