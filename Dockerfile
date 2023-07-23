FROM python:3.10-bullseye

WORKDIR /opt/app

COPY ./requirements.txt /opt/app
RUN pip install -r requirements.txt
COPY . /opt/app

CMD python3 start.py