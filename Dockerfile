FROM python:3.12
LABEL authors="2ilgan1601@gmail.com"

ENV PYTHOUNNBUFFERED 1

WORKDIR app/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python","manage.py","runserver","0.0.0.0:8000"]
