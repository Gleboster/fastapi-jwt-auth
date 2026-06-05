FROM python:3.12-alpine as base

WORKDIR /usr/app

COPY ./pyproject.toml ./uv.lock ./

RUN pip install uv
RUN uv sync --frozen

COPY . .

CMD [ "uv", "run", "python", "./main.py" ]

EXPOSE 8000

# docker run -v D:\MyProjects\PycharmProjects\auth_2.0\src:/usr/app/src --env-file .\.env -p 8090:8000 --rm app_dev