import argparse
import logging
import os

from kabeneko.web import app


ROOT_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(ROOT_DIR, 'static')


def main():
    parser = argparse.ArgumentParser()
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

    options.verbosity = logging.WARNING - (options.verbosity * 10)
    # Set our starting logging level
    logging.basicConfig(level=options.verbosity)

    app.config.options = options

    app.run(
        debug=(options.verbosity < logging.WARNING),
        host=options.host,
        port=options.port,
    )

if __name__ == "__main__":
    main()
