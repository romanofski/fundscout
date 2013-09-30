from fundscout.models import BankAccount
from fundscout.models import Currency
from fundscout.models import ImportBatch
from fundscout.models import Session
import csv
import datetime
import os.path


def import_csv(filepath):
    session = Session()
    bankaccount = guess_account_from_filename(filepath)
    if bankaccount is None:
        return
    with open(filepath, 'r') as csvfile:
        batch = ImportBatch.from_csv(session, csvfile)
        if batch is not None:
            batch.bank_account = bankaccount
            session.add(batch)
    session.commit()


def guess_account_from_filename(session, filename):
    """Returns the account instance by using the filename without
       extension.
    """
    # TODO: we need some kind of fulltext search here
    name = os.path.splitext(os.path.basename(filename))[0].lower()
    for ba in session.query(BankAccount).all():
        if ba.name in name:
            return ba
