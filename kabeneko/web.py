from flask import Flask, render_template
import logging

import os
from kabeneko import settings
from kabeneko.providers.teamcity import TeamCity
from kabeneko.images import Cats

logger = logging.getLogger(__name__)
app = Flask(__name__)

__root__ = os.path.dirname(__file__)
__static__ = os.path.join(__root__, 'static')


@app.route("/")
def index():
    tc = TeamCity(settings.TEAMCITY_WIDGET)

    successes, investigation, failures = tc.poll()

    cats = Cats(__static__).images()

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
    cats = Cats(__static__).images()
    return render_template('happy.html',
        cats=cats
        )


@app.route('/worried')
def worried():
    cats = Cats(__static__).images()
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
    cats = Cats(__static__).images()
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
