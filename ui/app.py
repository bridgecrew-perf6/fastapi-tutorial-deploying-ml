import streamlit as st
from annotated_text import annotated_text
import requests
from constants import EntityTypes, LOCAL_ENTITY_ENDPOINT


selected_language = st.sidebar.selectbox(
    'Select a language', options=['en', 'fr'])
entity_options = ['LOC', 'PER', 'ORG']
selected_entities = st.sidebar.multiselect(
    'Select the entities you want to detect',
    options=entity_options,
    default=entity_options,
)

text_input = st.text_area('Type a text to anonymize')

uploaded_file = st.file_uploader('or Upload a file', type=[
                                 'doc', 'docx', 'pdf', 'txt'])
if uploaded_file is not None:
    text_input = uploaded_file.getvalue()
    text_input = text_input.decode('utf-8')


def extract_tokens(tokens):
    normal_tokens, anonymized_tokens = [], []

    for t in tokens:
        common_name = t['common_name']
        text = t['text']
        anonymized_text = t['anonymized_text']

        if common_name == EntityTypes.PERSON:
            colour = '#faa'
        elif common_name == EntityTypes.LOCATION:
            colour = '#fda'
        elif common_name == EntityTypes.ORGANIZATION:
            colour = '#afa'
        else:
            normal_tokens.append(' ' + text + ' ')
            anonymized_tokens.append(' ' + text + ' ')
            continue

        normal_tokens.append((text, common_name, colour))
        anonymized_tokens.append((anonymized_text, common_name, colour))

    return normal_tokens, anonymized_tokens


def call(text_input, selected_entities, selected_language):
    request_body = {
        'text': text_input,
        'model_language': selected_language,
        'model_size': 'sm',
        'selected_entities': selected_entities
    }

    response = requests.post(
        f'http://{LOCAL_ENTITY_ENDPOINT}', json=request_body)
    response = response.json()
    print(response)

    normal_tokens, anonymized_tokens = extract_tokens(response['tokens'])
    annotated_text(*normal_tokens)
    st.markdown('**Anonymized text**')
    annotated_text(*anonymized_tokens)


if st.button('Anonymize'):
    if len(text_input) > 0:
        call(text_input, selected_entities, selected_language)
