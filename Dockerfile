FROM python:alpine3.13

WORKDIR /opt/app

COPY ./src .
COPY ./requirements.txt .

RUN python -m venv /opt/app/src/venv

ENV PATH="/opt/app/src/venv/bin:$PATH"

RUN python -m pip install -U pip

RUN python -m pip install -r requirements.txt

ENTRYPOINT [ "python3", "main.py" ]