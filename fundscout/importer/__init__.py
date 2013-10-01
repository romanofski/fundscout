from fundscout.models import BankAccount
from fundscout.models import ImportBatch
from fundscout.models import Session
import csv
import datetime
import os.path


def import_csv(session, filepath, bankaccount):
    tx_imported = 0
    if bankaccount:
        with open(filepath, 'r') as csvfile:
            batch = ImportBatch.from_csv(session, csvfile)
            if batch is not None:
                batch.bank_account = bankaccount
                session.add(batch)
                tx_imported = len(batch.transactions)
        session.commit()
    return tx_imported


def guess_accountname_from_filename(filename):
    """Returns the account name instance by using the filename without
       extension.
    """
    # TODO: we need some kind of fulltext search here
    return os.path.splitext(os.path.basename(filename))[0].lower()
