FROM python:3.7.6
RUN mkdir /app
COPY ./requirements.txt  /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV FLASK_APP=app.py
CMD python -m flask run --host=0.0.0.0
