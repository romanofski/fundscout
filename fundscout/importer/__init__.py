from fundscout.models import BankAccount
from fundscout.models import Currency
from fundscout.models import ImportBatch
from fundscout.models import Session
import csv
import datetime
import os.path


def import_csv(filepath):
    tx_imported = 0
    session = Session()
    bankaccount = guess_account_from_filename(session, filepath)
    if bankaccount:
        with open(filepath, 'r') as csvfile:
            batch = ImportBatch.from_csv(session, csvfile)
            if batch is not None:
                batch.bank_account = bankaccount
                session.add(batch)
                tx_imported = len(batch.transactions)
        session.commit()
    return tx_imported


def guess_account_from_filename(session, filename):
    """Returns the account instance by using the filename without
       extension.

       .. note:: If no bank account with guessed name can be found, a new one with
       default values is created. This is subject to change in future
       versions.
    """
    # TODO: we need some kind of fulltext search here
    name = os.path.splitext(os.path.basename(filename))[0].lower()
    result = session.query(BankAccount).filter_by(name=name).first()
    if result is None and name:
        result = create_bank_account(name)
        session.add(result)
        session.flush()
    return result


def create_bank_account(name, **kwargs):
    return BankAccount(name=name,
                       description=name,
                       currency=Currency(name='Dollar', isoname='AUD'))
