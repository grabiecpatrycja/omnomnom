FROM ubuntu:latest
RUN apt update
RUN apt upgrade -y
RUN apt install python3 python3-pip -y

COPY . /code
WORKDIR /code
RUN pip install -r requirements.txt

CMD python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000