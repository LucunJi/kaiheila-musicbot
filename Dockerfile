# credits https://superuser.com/questions/1223118/emulating-microphone-input-to-chrome-inside-docker-container

FROM selenium/standalone-chrome:4.0.0-rc-1-20210902

USER root

# install necessary packages
RUN apt-get -qq update && apt-get install -y pulseaudio

USER seluser

# copy over music files
COPY test-musics /opt/

# use custom entrypoint
COPY entrypoint.sh /opt/bin/entrypoint.sh

ENTRYPOINT /opt/bin/entrypoint.sh