import argparse
import fundscout
import fundscout.importer.config
import getpass
import os
import os.path
import sys


def _setup_commandline_arguments():
    """ Helper method to setup arguments and argument parser. """
    parser = argparse.ArgumentParser(
        description='{name} {version} -- {description}'.format(
            name=fundscout.__name__, version=fundscout.__version__,
            description=fundscout.__description__))

    parser.add_argument(
        "--database",
        help=("Path to an SQL lite database. If no path is given a new"
              " one is created."
              ),
        type=str,
        default=os.path.join(os.path.abspath(os.getcwd()), 'fundscout.sqlite')
    )
    parser.add_argument(
        "--config",
        help=("Path to configuration file for importing."),
        type=str
    )
    return parser


def client():
    """ Imports new data into the given database."""
    parser = _setup_commandline_arguments()
    arguments = parser.parse_args()

    if arguments.config and os.path.exists(arguments.config):
        fundscout.importer.config.configure_and_run(arguments.config)

    sys.exit(0)
