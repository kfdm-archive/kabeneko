from flask import Flask, render_template
import argparse
import time
import logging
import glob
import os
from kabeneko import settings
from providers.teamcity import TeamCity

logger = logging.getLogger(__name__)
app = Flask(__name__)

__root__ = os.path.dirname(__file__)
__static__ = os.path.join(__root__, 'static')


def find_cats():
    current_day = int(time.strftime('%j'))

    todays_cats = {
        'sad': '',
        'worried': '',
        'happy': '',
    }

    all_cats = {
        'sad': glob.glob('%s/sad/*' % __static__),
        'worried': glob.glob('%s/worried/*' % __static__),
        'happy': glob.glob('%s/happy/*' % __static__),
        }

    logger.info('All cats: %s', all_cats)

    for k in all_cats:
        if len(all_cats[k]) == 0:
            continue
        i = current_day % len(all_cats[k])
        cat = all_cats[k][i].split('/static/').pop()
        todays_cats[k] = cat

    logger.info('Today\'s cats: %s', todays_cats)
    return todays_cats


@app.route("/")
def index():
    tc = TeamCity(settings.TEAMCITY_WIDGET)

    successes, investigation, failures = tc.poll()

    cats = find_cats()

    if len(failures) > 0:
        return render_template(
            'sad.html',
            failures=failures,
            cats=cats
            )
    if len(investigation) > 0:
        return render_template('worried.html',
            investigation=investigation,
            cats=cats
            )
    return render_template('happy.html',
        cats=cats
        )


@app.route('/success')
def success():
    cats = find_cats()
    return render_template('happy.html',
        cats=cats
        )


@app.route('/worried')
def worried():
    cats = find_cats()
    investigation = [{
            'group': 'Project Team',
            'project': 'Build Configuration',
            'build': '000',
            'date': 'timestamp goes here',
            'status': 'An engineer is currently investigating the failure',
    }]
    return render_template('worried.html',
        investigation=investigation,
        cats=cats
        )


@app.route('/fail')
def fail():
    cats = find_cats()
    failures = [{
            'group': 'group',
            'project': 'project',
            'build': '000',
            'date': 'timestamp goes here',
            'status': 'has failed',
    }]
    return render_template(
        'sad.html',
        failures=failures,
        cats=cats
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbosity',
        action='count',
        help='Verbosity level',
        default=0
    )
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', default=8000, type=int)
    options = parser.parse_args()

    options.verbosity = logging.WARNING - (options.verbosity * 10)
    # Set our starting logging level
    logging.basicConfig(level=options.verbosity)

    app.run(
        debug=(options.verbosity < logging.WARNING),
        host=options.host,
        port=options.port,
        )

if __name__ == "__main__":
    main()
