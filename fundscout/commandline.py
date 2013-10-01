from fundscout.models import Base
from fundscout.models import Session
from fundscout.models import BankAccount
import argparse
import fundscout
import fundscout.importer.config
import getpass
import os
import os.path
import sqlalchemy
import sys
import urllib
import urlparse


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
        default='sqlite:///' + os.path.join(os.path.abspath(os.getcwd()), 'fundscout.sqlite')
    )
    parser.add_argument(
        "--list-accounts",
        help="Lists the accounts found in the database.",
        action='store_true',
    )
    parser.add_argument(
        "--config",
        help=("Path to configuration file for importing."),
        type=str
    )
    parser.add_argument(
        "--csv",
        help=("Path to a csv file for importing."),
        type=str
    )
    return parser


def client():
    """ Imports new data into the given database."""
    parser = _setup_commandline_arguments()
    arguments = parser.parse_args()

    engine = sqlalchemy.create_engine(arguments.database)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    Session.configure(bind=engine)
    session = Session()

    if arguments.list_accounts:
        names = [x.name for x in session.query(BankAccount).all()]
        print '\n'.join(names)

    if arguments.config and os.path.exists(arguments.config):
        fundscout.importer.config.configure_and_run(arguments.config)

    if arguments.csv and os.path.exists(arguments.csv):
        ba_name = fundscout.importer.guess_accountname_from_filename(
            arguments.csv)
        bankaccount = BankAccount.find_by_name(session, ba_name)
        if bankaccount is None:
            print 'Unable to find Bankaccount {}'.format(ba_name)
        else:
            print '{} transactions imported.'.format(
                fundscout.importer.import_csv(session,
                                              arguments.csv,
                                              bankaccount))

    sys.exit(0)
