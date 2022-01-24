from fastapi import FastAPI

from copy import deepcopy

from langcodes import Language
from data_models import EntityOut, EntitiesOut, UserRequestIn
import spacy
from typing import Dict, List, Tuple

app = FastAPI()


def load_models() -> Dict[str, Language]:
    """
    Loads the models from disk.

    Returns:
        Dictionary of loaded models.
    """
    # Run the following to download the models
    # python -m spacy download en_core_web_sm
    # python -m spacy download fr_core_news_sm

    models = {
        'en_sm': spacy.load('en_core_web_sm'),
        'fr_sm': spacy.load('fr_core_news_sm')
    }

    return models


models = load_models()


@app.get('/')
def read_root():
    return {'message': 'Welcome from the Anonymization API'}


@app.post('/entities', response_model=EntitiesOut)
def extract_entities(user_request: UserRequestIn):
    text = user_request.text
    language = user_request.model_language
    model_size = user_request.model_size
    selected_entities = user_request.selected_entities

    model_key = language + '_' + model_size
    model = models[model_key]

    tokens, anonymized_text = process_document(text, model, selected_entities)

    return {
        'tokens': tokens,
        'anonymized_text': anonymized_text
    }


def process_document(text, model, selected_entities) -> Tuple[List[EntityOut], str]:
    def anonymize(text: str):
        return 'X' * len(text)

    document = model(text)
    tokens: List[EntityOut] = []
    anonymized_text = list(deepcopy(text))

    for token in document:
        token_data = EntityOut(
            text=token.text, entity_type=token.ent_type_, start_idx=token.idx)

        start = token_data.start_idx
        end = start + len(token.text)

        if (token.ent_type_ == 'PERSON') & ('PER' in selected_entities):
            token_data.common_name = 'Person'
            token_data.anonymized_text = anonymize(token.text)
            anonymized_text[start:end] = token_data.anonymized_text
        elif (token.ent_type_ in ['GPE', 'LOC']) & ('LOC' in selected_entities):
            token_data.common_name = 'Location'
            token_data.anonymized_text = anonymize(token.text)
            anonymized_text[start:end] = token_data.anonymized_text
        elif (token.ent_type_ == 'ORG') & ('ORG' in selected_entities):
            token_data.common_name = 'Organization'
            token_data.anonymized_text = anonymize(token.text)
            anonymized_text[start:end] = token_data.anonymized_text

        tokens.append(token_data)

    anonymized_text = ''.join(anonymized_text)

    return tokens, anonymized_text
