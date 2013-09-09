import csv
from fundscout.models import BankAccount
from fundscout.models import Currency
from fundscout.models import FundTransaction
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
    session.add(bankaccount)
    with open(filepath, 'r') as csvfile:
        transactions = []
        for row in csv.reader(csvfile):
            if not row:
                continue
            tx = FundTransaction(description=row[-1],
                                 amount=row[1],
                                 effective=datetime.datetime.strptime(row[0], '%d/%m/%Y')
                                )
            transactions.append(tx)
        bankaccount.import_transactions(transactions)
    session.commit()
