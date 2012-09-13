from flask import Flask, render_template
import xml.etree.cElementTree as ET
import argparse
import time
import requests
import logging
import glob
import os
from TeamcityCat import settings

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
    successes = []
    investigation = []
    failures = []

    cats = find_cats()

    try:
        req = requests.get(settings.TEAMCITY_WIDGET)

        if req.status_code is not 200:
            raise IOError("Error loading feed")

        content = """<?xml version="1.0" encoding="UTF-8"?><root>%s</root>""" % req.text.replace('&', '&amp;')
        doc = ET.fromstring(content)

        # Loop through each project
        for table in doc.findall('table'):

            group = None
            for a in table.findall('tr/td/div/a'):
                if a.attrib.get('class') == 'buildTypeName':
                    group = a.text
            for tr in table.findall('tr'):
                entry = {
                    'project': None,
                    'build': None,
                    'status': None,
                    'group': group
                }

                # loop through each build config
                for td in tr.findall('td'):
                    # Get success status
                    if td.attrib.get('class') == 'buildConfigurationName':
                        entry['project'] = td.find('a').text
                        entry['status'] = td.find('img').attrib['title']
                    if td.attrib.get('class') == 'buildNumberDate':
                        entry['build'] = td.find('div/a').text

                # Skip project rows
                if entry['status'] is None:
                    continue

                if 'success' in entry['status']:
                    successes.append(entry)
                elif 'investigating' in entry['status']:
                    investigation.append(entry)
                else:
                    failures.append(entry)

    except Exception, e:
        logger.exception('Exception found while loading feeds')
        failures.append({
            'project': '?',
            'build': e,
            'group': '?',
            })

    for success in successes:
        logging.info('Success: %(group)15s : %(project)-30s %(build)s' % success)
    for warning in investigation:
        logging.warning('Investigation: %(group)15s : %(project)-30s %(build)s' % warning)
    for failure in failures:
        logging.error('Failure: %(group)15s : %(project)-30s %(build)s' % failure)

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
