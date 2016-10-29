from ..models.models import DBSession, UserAccount, BankAccount, Costumer, OwnerBankaccount, Transaction, RepeatPayment
import datetime
from dateutil.relativedelta import relativedelta

import time


def paying():
    allrepeat = DBSession.query(RepeatPayment).order_by(RepeatPayment.nexttime)
    for repeatpay in allrepeat :
        now = datetime.datetime.now()
        repaytime = repeatpay.nexttime
        if repaytime.year == now.year and repaytime.month == now.month and repaytime.day == now.day :
            bank = DBSession.query(BankAccount).filter(BankAccount.accountid == repeatpay.myaccount).first()
            bankto = DBSession.query(BankAccount).filter(BankAccount.accountid == repeatpay.accountdes).first()

            bank.balance -= repeatpay.money
            DBSession.add(Transaction(BankAccount_id = bank.accountid, datetime = datetime.datetime.now(),
                                    types = 'Auto Pay-', money =  repeatpay.money, balance = bank.balance, detail = 'to '+bankto.accountname))

            bankto.balance += repeatpay.money
            DBSession.add(Transaction(BankAccount_id = bankto.accountid, datetime = datetime.datetime.now(),
                                    types = 'Auto Pay+', money =  repeatpay.money, balance = bankto.balance, detail = 'from '+bank.accountname))

            repeatpay.nexttime += relativedelta(days=+ repeatpay.nextday, months=+ repeatpay.nextmonth, years=+ repeatpay.nextyear)
