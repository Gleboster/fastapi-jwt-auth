FROM python:3.12-alpine as base

WORKDIR /usr/src/app

RUN python -m pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "./main.py" ]

EXPOSE 8000