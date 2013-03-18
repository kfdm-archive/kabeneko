import argparse
import logging
import os

from kabeneko.web import app
from kabeneko.settings import Config


ROOT_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(ROOT_DIR, 'static')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config')
    parser.add_argument(
        '-v',
        '--verbosity',
        action='count',
        help='Verbosity level',
        default=0
    )
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', default=8000, type=int)
    parser.add_argument(
        '--images',
        default=STATIC_DIR,
        help='Path to static images (Defaults to packaged images)'
    )
    options = parser.parse_args()
    # Set our default logging here based on the first pass of arguments
    logging.basicConfig(level=(logging.WARNING - (options.verbosity * 10)))

    if options.config:
        logging.basicConfig(level=logging.DEBUG)
        logging.root.setLevel(logging.DEBUG)
        settings = Config(options.config)
        parser.set_defaults(**settings.defaults())
        options = parser.parse_args()
    else:
        settings = Config()

    # Reset our logging level in case things have changed
    logging.root.setLevel(logging.WARNING - (options.verbosity * 10))

    app.config.options = options
    app.config.settings = settings

    app.run(
        debug=(options.verbosity < logging.WARNING),
        host=options.host,
        port=options.port,
    )

if __name__ == "__main__":
    main()
