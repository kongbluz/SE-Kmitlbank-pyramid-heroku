from ..models.models import DBSession, UserAccount, BankAccount, Costumer, OwnerBankaccount, Transaction, RepeatPayment
import datetime

import time

def paying(self):
    time.sleep(86400)
    allrepeat = DBSession.query(RepeatPayment).order_by(RepeatPayment.nexttime)
    for repeatpay in allrepeat :
        now = datetime.datetime.now()
        repaytime = repeatpay.nexttime
        if repaytime.year == now.year and repaytime.month == now.month and repaytime.day == now.day :
            bank = DBSession.query(BankAccount).filter(BankAccount.accountid == repeatpay.myaccount).first()
            bankto = DBSession.query(BankAccount).filter(BankAccount.accountid == repeatpay.accountdes).first()

            bank.balance -= money
            DBSession.add(Transaction(BankAccount_id = bank.accountid, datetime = datetime.datetime.now(),
                                      types = 'Auto Pay-', money = money, balance = bank.balance, detail = 'to '+bankto.accountname))

            bankto.balance += money
            DBSession.add(Transaction(BankAccount_id = bankto.accountid, datetime = datetime.datetime.now(),
                                      types = 'Auto Pay+', money = money, balance = bankto.balance, detail = 'from '+bank.accountname))

            repeatpay.nexttime.year += repeatpay.repaytime.year
            repeatpay.nexttime.month += repeatpay.repaytime.month
            repeatpay.nexttime.day += repeatpay.repaytime.day
