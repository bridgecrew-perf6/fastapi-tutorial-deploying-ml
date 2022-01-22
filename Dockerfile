FROM python:3.8
RUN pip install --upgrade pip

WORKDIR /app

# bundle api source to app
COPY ../ /app
ENV PYTHONPATH=/app

# install dependencies
RUN pip install -r requirements.txt

# download models from spaCy
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download fr_core_news_sm
# check if the installed models are compatible and if not, print details on how to update them
RUN python -m spacy validate

# expose port for uvicorn
EXPOSE 8000

# run uvicorn
WORKDIR /app/api
ENTRYPOINT [ "uvicorn" ]
CMD ["main:app", "--host", "0.0.0.0"]
