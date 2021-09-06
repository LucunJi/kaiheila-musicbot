docker run -d --shm-size=2g -v $PWD/test-musics:/app/test-musics:ro --env-file botcfg.env --name kaiheila-musicbot lucunji/kaiheila-musicbot
