FROM ubuntu:latest

WORKDIR /home/server/
RUN apt-get update && apt-get install -y \
    python3-pip
RUN apt-get install -y python3-psycopg2
RUN apt-get install -y libpq-dev python-dev

COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY . .

CMD [ "python3", "server.py" ]