FROM python:3.10

COPY ./tracker_core/requirements.txt /

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY ./tracker_core/ /app

WORKDIR /app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]