import logging
import logging.config

from configs import BotConfigs, GeneralConfigs, DEFAULT_LOG_FORMAT, DEFAULT_LOG_DATEFMT
from selenium_controller import SeleniumController

logger: logging.Logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(format=DEFAULT_LOG_FORMAT, datefmt=DEFAULT_LOG_DATEFMT, level=logging.INFO)
    logger.info('read configs')
    config_general = GeneralConfigs()
    logging.basicConfig(level=config_general.log_level)
    config_bot = BotConfigs()

    with SeleniumController(config_bot, config_general) as controller:
        controller.join_voice_channel()
        controller.keep_session()


if __name__ == '__main__':
    main()
    input('press any key to quit...')
