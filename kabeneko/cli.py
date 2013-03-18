import argparse
import logging

from kabeneko.web import app


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
