import logging
import logging.config
import time

from configs import BotConfigs, GeneralConfigs, DEFAULT_LOG_FORMAT, DEFAULT_LOG_DATEFMT
from selenium_controller import SeleniumController

logger: logging.Logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(format=DEFAULT_LOG_FORMAT, datefmt=DEFAULT_LOG_DATEFMT, level=logging.INFO)
    logging.getLogger().setLevel(logging.INFO)
    logger.info('read configs')
    config_general = GeneralConfigs()
    logging.basicConfig(level=config_general.log_level)
    logging.getLogger().setLevel(config_general.log_level)
    config_bot = BotConfigs()

    SeleniumController(config_bot, config_general).join_voice_channel()


if __name__ == '__main__':
    main()
    # multi-thread code is not written yet, so just make an infinite loop
    while True:
        time.sleep(10)
