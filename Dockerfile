# credits https://superuser.com/questions/1223118/emulating-microphone-input-to-chrome-inside-docker-container

FROM ubuntu:focal-20210827

WORKDIR /app

USER root

# install prerequisites
RUN apt-get update
RUN apt-get install -y wget
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata

# install chrome
RUN wget -q -O /tmp/chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_93.0.4577.63-1_amd64.deb
RUN apt-get install -y /tmp/chrome.deb
RUN rm /tmp/chrome.deb

# install chrome driver
RUN apt-get install -y unzip
RUN wget -q -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/93.0.4577.15/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip -d /usr/bin
RUN rm /tmp/chromedriver.zip

# install python requirements
RUN apt-get -y install python3-pip
RUN pip install pipenv

# install PulseAudio
RUN apt-get install -y pulseaudio

RUN useradd -ms /bin/bash khlbot
USER khlbot

COPY entrypoint.sh /opt/bin/entrypoint.sh
# RUN chmod +x /opt/bin/entrypoint.sh

# copy the Pipfile first to better utilize docker cache
COPY selenium_bot/Pipfile selenium_bot/Pipfile.lock /app/
RUN pipenv install --system --deploy --ignore-pipfile

COPY test-musics/ /app/test-musics/
COPY selenium_bot/ /app/

# prevent chrome crash
ENV DISPLAY=:98

ENTRYPOINT /opt/bin/entrypoint.sh
