FROM python:3.12-alpine as base

WORKDIR /usr/app

RUN python -m pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src
COPY ./main.py ./main.py

ENTRYPOINT [ "python", "./main.py" ]
# docker run --rm --env-file .env app_prod