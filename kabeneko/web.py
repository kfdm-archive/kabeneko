from flask import Flask, render_template

from kabeneko.providers.teamcity import TeamCity
from kabeneko.images import Cats

app = Flask(__name__)


@app.route("/")
def index():
    tc = TeamCity(app.config.settings.get('teamcity.url'))

    successes, investigation, failures = tc.poll()

    cats = Cats(app.config.options.images).images()

    if len(failures) > 0:
        return render_template(
            'sad.html',
            failures=failures,
            cats=cats
        )
    if len(investigation) > 0:
        return render_template(
            'worried.html',
            investigation=investigation,
            cats=cats
        )
    return render_template(
        'happy.html',
        cats=cats
    )


@app.route('/success')
def success():
    cats = Cats(app.config.options.images).images()
    return render_template(
        'happy.html',
        cats=cats
    )


@app.route('/worried')
def worried():
    cats = Cats(app.config.options.images).images()
    investigation = [{
        'group': 'Project Team',
        'project': 'Build Configuration',
        'build': '000',
        'date': 'timestamp goes here',
        'status': 'An engineer is currently investigating the failure',
    }]
    return render_template(
        'worried.html',
        investigation=investigation,
        cats=cats
    )


@app.route('/fail')
def fail():
    cats = Cats(app.config.options.images).images()
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
