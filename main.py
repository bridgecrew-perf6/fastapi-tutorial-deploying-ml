from pathlib import Path
from fastapi import FastAPI

from copy import deepcopy
from data_models import EntitiesOut, UserRequestIn
import spacy


app = FastAPI()


def load_models():
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


@app.post('/entities', response_model=EntitiesOut)
def extract_entities(user_request: UserRequestIn):
    text = user_request.text
    language = user_request.model_language
    model_size = user_request.model_size

    model_key = language + '_' + model_size

    model = models[model_key]

    doc = model(text)

    entities = [
        {
            'start': ent.start_char,
            'end': ent.end_char,
            'type': ent.label_,
            'text': ent.text,
        }
        for ent in doc.ents
    ]

    anonymized_text = list(deepcopy(text))

    for entity in entities:
        start = entity['start']
        end = entity['end']
        anonymized_text[start:end] = 'X' * (end - start)

    anonymized_text = ''.join(anonymized_text)

    return {'entities': entities, 'anonymized_text': anonymized_text}
