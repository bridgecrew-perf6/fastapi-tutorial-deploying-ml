Based on this [tutorial](https://towardsdatascience.com/how-to-deploy-a-machine-learning-model-with-fastapi-docker-and-github-actions-13374cbd638a).

# Description
some text, some pictures

# Installation
## Local
1. Make a virtual env.
2. Install dependencies: `pip install -r requirements.txt`
3. Install spacy models:
- `python -m spacy download en_core_web_sm`
- `python -m spacy download fr_core_news_sm`
5. Check if the installed models are compatible and if not, print details on how to update them: `python -m spacy validate`

## Docker
1. `docker-compose up --build`
2. go to `127.0.0.1:8000/docs` to interact with api
