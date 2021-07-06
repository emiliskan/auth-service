FROM python:3.9
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONPATH "${PYTHONPATH}:/app/"
ARG POETRY_PARAMS="--no-dev"

RUN apt update && apt -y upgrade && apt install -y python3-setuptools netcat

ENV PATH="${PATH}:/root/.local/bin"
RUN pip install --user poetry==1.0.*

RUN mkdir /app
COPY poetry.lock pyproject.toml /app/
WORKDIR /app/
RUN poetry install $POETRY_PARAMS --no-interaction --no-ansi
COPY / /app/

CMD python app.py
