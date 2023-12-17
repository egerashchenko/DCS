FROM ubuntu:latest

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3-pip

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python3","main.py"]

