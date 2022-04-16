FROM python:3

WORKDIR /usr/src/
RUN pip3 install poetry && poetry config virtualenvs.in-project true

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install

COPY . .

EXPOSE 80
CMD poetry run python -m main
