FROM joyzoursky/python-chromedriver:3.9
ENV PYTHONUNBUFFERED 1
RUN mkdir /ZMTeam
COPY ./requirements.txt /ZMTeam/requirements.txt
RUN pip install -r ZMTeam/requirements.txt

COPY . /ZMTeam
WORKDIR /ZMTeam
ENV PYTHONPATH "${PYTHONPATH}:/ZMTeam"

#RUN apk update && apk upgrade
#RUN apk add unzip
#RUN apk add wget
#RUN wget -O /yandex.zip https://github.com/yandex/YandexDriver/releases/download/v23.3.1-stable/yandexdriver-23.3.1.755-linux.zip
#RUN mkdir /webdrivers
#RUN unzip /yandex.zip -d /webdrivers
#RUN rm /yandex.zip
# https://github.com/joyzoursky/docker-python-chromedriver/blob/master/py-debian/3.9/Dockerfile
