docker run -d --shm-size=2g -e TZ="America/Chicago" -v $PWD/test-musics:/app/test-musics:ro --name kaiheila-musicbot lucunji/kaiheila-musicbot
