from enum import Enum


class EntityTypes(str, Enum):
    PERSON = 'Person'
    LOCATION = 'Location'
    ORGANIZATION = 'Organization'


# API parameters
API_IP = 'backend'
PORT = '8000'
ENTITY_PATH = 'entities'
LOCAL_ENTITY_ENDPOINT = f'{API_IP}:{PORT}/{ENTITY_PATH}'
