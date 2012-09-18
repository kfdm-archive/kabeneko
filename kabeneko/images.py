import glob
import logging
import time

logger = logging.getLogger(__name__)


class Cats(object):
    def __init__(self, static_path):
        self.path = static_path

    def find_cats(self):
        current_day = int(time.strftime('%j'))

        todays_cats = {
            'sad': '',
            'worried': '',
            'happy': '',
        }

        all_cats = {
            'sad': glob.glob('%s/sad/*' % self.path),
            'worried': glob.glob('%s/worried/*' % self.path),
            'happy': glob.glob('%s/happy/*' % self.path),
            }

        logger.info('Happy cats: %s', all_cats['happy'])
        logger.info('Sad cats: %s', all_cats['sad'])
        logger.info('Worried cats: %s', all_cats['worried'])

        for k in all_cats:
            if len(all_cats[k]) == 0:
                continue
            i = current_day % len(all_cats[k])
            cat = all_cats[k][i].split('/static/').pop()
            todays_cats[k] = cat

        logger.info('Today\'s cats: %s', todays_cats)
        return todays_cats

    def images(self):
        return self.find_cats()
