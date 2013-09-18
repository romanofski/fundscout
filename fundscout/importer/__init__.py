import csv
from fundscout.models import BankAccount
from fundscout.models import Currency
from fundscout.models import ImportBatch
from fundscout.models import Session
import datetime


def import_csv(filepath, accountname='anz'):
    session = Session()
    bankaccount = session.query(BankAccount).filter_by(name=accountname).first()
    if bankaccount is None:
        bankaccount = BankAccount(
            name=accountname, currency=Currency(name='Australian Dollar',
                                                isoname='AUD')
        )
    with open(filepath, 'r') as csvfile:
        batch = ImportBatch.from_csv(session, csvfile)
        if batch is not None:
            batch.bank_account = bankaccount
            session.add(batch)
    session.commit()
