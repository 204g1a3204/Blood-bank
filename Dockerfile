FROM python:3.10.0a6-alpine3.14

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" , "manage.py" , "runserver" , "0.0.0.0:8000" ]