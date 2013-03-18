import logging
from ConfigParser import RawConfigParser

logger = logging.getLogger(__name__)

__all__ = ['Config']


DEFAULTS = {
    'teamcity': {
        'url': 'http://localhost:8111/externalStatus.html'
    }
}


class Config(object):
    def __init__(self, path=None):
        self.config = RawConfigParser()
        if path:
            logger.info('Loading settings from %s', path)
            self.config.read(path)
        else:
            logger.info('Using default settings')

    def defaults(self):
        return {
            'teamcity': 'http://localhost:8111/externalStatus.html'
        }

    def get(self, key, default=None):
        section, option = key.split('.', 1)
        if self.config.has_option(section, option):
            return self.config.get(section, option)
        return DEFAULTS[section][option]
