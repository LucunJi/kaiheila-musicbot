# credits https://superuser.com/questions/1223118/emulating-microphone-input-to-chrome-inside-docker-container

FROM selenium/standalone-chrome:4.0.0-rc-1-20210902

WORKDIR /app

USER root

RUN apt-get -qq update
RUN apt-get -y install python3-pip
RUN pip install pipenv

USER seluser

COPY entrypoint.sh /opt/bin/entrypoint.sh
# RUN chmod +x /opt/bin/entrypoint.sh

# copy the Pipfile first to better utilize docker cache
COPY selenium_bot/Pipfile selenium_bot/Pipfile.lock /app/
RUN pipenv install --system --deploy --ignore-pipfile

COPY selenium_bot/ /app/

ENTRYPOINT /opt/bin/entrypoint.sh
