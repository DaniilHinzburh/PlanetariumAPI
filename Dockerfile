FROM python:3.12
LABEL authors="2ilgan1601@gmail.com"

ENV PYTHOUNNBUFFERED 1

WORKDIR docker_planetarium/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p /files/media

RUN adduser \
    --disabled-password \
    --no-create-home \
    my_user

RUN chown -R my_user /files/media
RUN chmod -R 755 /files/media

USER my_user