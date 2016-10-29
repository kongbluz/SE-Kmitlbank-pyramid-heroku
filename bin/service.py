from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
    Everyone
    )

from .models.models import DBSession, UserAccount, BankAccount, Costumer, OwnerBankaccount, Transaction
from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config
    )
import datetime
from .scripts.genOTP import GETOTP
import simplejson as json

class service(object):
    def __init__(self, request):
        self.request = request

    @view_config(route_name='trade', renderer='json')
    def trade(self):
        request = self.request
        try:
            username    = request.GET['user']
            accountfrom = request.GET['account']
            accountdes  = request.GET['accountdes']
            otp         = request.GET['otp']
            money       = request.GET['money']
        except Exception:
            return { 'status' : False,
                     'detail' : 'do not have some attribute'
                   }
        if accountfrom == accountdes :
            return { 'status' : False,
                     'detail' : 'do not send to same username'
                   }

        user = DBSession.query(UserAccount).filter(UserAccount.username == username).first()
        if user is None :
            return { 'status' : False,
                     'detail' : 'do not have this username'
                   }
        owner = DBSession.query(OwnerBankaccount).filter(OwnerBankaccount.BankAccount_id == accountfrom).filter(OwnerBankaccount.UserAccount_id == user.userid).first()
        if owner is None :
            return { 'status' : False,
                     'detail' : 'wrong bank account'
                   }

        bankto = DBSession.query(BankAccount).filter(BankAccount.accountid == accountdes).first()
        if bankto is None :
            return { 'status' : False,
                     'detail' : 'wrong destination account'
                   }

        bank = DBSession.query(BankAccount).filter(BankAccount.accountid == owner.BankAccount_id).first()
        if owner.otppassword != otp :
            return { 'status' : False,
                     'detail' : 'Wrong otp password'
                   }
        try:
            money = float(money)
        except Exception:
            return { 'status' : False,
                     'detail' : 'not money type'
                   }
        if money < 0 :
            return { 'status' : False,
                     'detail' : 'not money type'
                   }
        elif bank.balance - money < 0 :
            return { 'status' : False,
                     'detail' : 'do not have money enough'
                   }

        bank.balance -= money
        DBSession.add(Transaction(BankAccount_id = bank.accountid, datetime = datetime.datetime.now(),
                                  types = 'Online Shopping-', money = money, balance = bank.balance, detail = 'to '+bankto.accountname))

        bankto.balance += money
        DBSession.add(Transaction(BankAccount_id = bankto.accountid, datetime = datetime.datetime.now(),
                                  types = 'Online Shopping+', money = money, balance = bankto.balance, detail = 'from '+bank.accountname))
        owner.otppassword = None
        return { 'status' : True,
                 'detail' : 'Success to Shopping'
               }

    @view_config(route_name='addpp', renderer='json')
    def addpp(self):
        request = self.request
        try:
            account  = request.GET['account']
            otppassword = request.GET['otp']
        except Exception:
            return { 'status' : False,
                     'detail' : 'do not have some attribute'
                   }
        myaccount = DBSession.query(OwnerBankaccount).filter(OwnerBankaccount.BankAccount_id == account).first()
        if myaccount is None:
            return { 'status' : False,
                     'detail' : 'wrong Bank Account'
                   }

        if myaccount.otppassword == otppassword :
            myaccount.passcodepp = GETOTP() + GETOTP()
            myaccount.otppassword = None
            bank      = DBSession.query(BankAccount).filter(BankAccount.accountid == account).first()
            costumer  = DBSession.query(Costumer).filter(Costumer.costumerid == bank.Costumer_id).first()
            return { 'status' : True,
                     'detail' : 'Success to add prompay',
                     'passcode' : myaccount.passcodepp,
                     'name' : costumer.fullname,
                     'accountname' : bank.accountname,
                     'accountid' : bank.accountid,
                     'nationid' : costumer.nationid,
                     'phonenumber' : costumer.phonenummber
                   }
        else :
            return { 'status' : False,
                     'detail' : 'Wrong otppassword'
                   }

    @view_config(route_name='tradepp', renderer='json')
    def tradepp(self):
        request = self.request
        try:
            accountfrom = request.GET['account']
            accountdes  = request.GET['accountdes']
            passcode    = request.GET['passcode']
            money       = request.GET['money']
        except Exception:
            return { 'status' : False,
                     'detail' : 'do not have some attribute'
                   }


        if accountfrom == accountdes :
            return { 'status' : False,
                     'detail' : 'do not send to same username'
                   }

        owner = DBSession.query(OwnerBankaccount).filter(OwnerBankaccount.BankAccount_id == accountfrom).first()
        if owner is None :
            return { 'status' : False,
                     'detail' : 'wrong bank account'
                   }

        bankto = DBSession.query(BankAccount).filter(BankAccount.accountid == accountdes).first()
        if bankto is None :
            return { 'status' : False,
                     'detail' : 'wrong destination account'
                   }

        bank = DBSession.query(BankAccount).filter(BankAccount.accountid == owner.BankAccount_id).first()
        if owner.passcodepp != passcode :
            return { 'status' : False,
                     'detail' : 'Wrong passcode'
                   }
        try:
            money = float(money)
        except Exception:
            return { 'status' : False,
                     'detail' : 'not money type'
                   }
        if money <= 0 :
            return { 'status' : False,
                     'detail' : 'not money type'
                   }
        elif bank.balance - money < 0 :
            return { 'status' : False,
                     'detail' : 'do not have money enough'
                   }

        bank.balance -= money
        DBSession.add(Transaction(BankAccount_id = bank.accountid, datetime = datetime.datetime.now(),
                                  types = 'Prompay-', money = money, balance = bank.balance, detail = 'to '+bankto.accountname))

        bankto.balance += money
        DBSession.add(Transaction(BankAccount_id = bankto.accountid, datetime = datetime.datetime.now(),
                                  types = 'Prompay+', money = money, balance = bankto.balance, detail = 'from '+bank.accountname))
        owner.otppassword = None

        transactions = DBSession.query(Transaction).filter(Transaction.BankAccount_id == bank.accountid).order_by(Transaction.transactionid.desc()).first()

        return { 'status' : True,
                 'detail' : 'Success to Shopping',
                 'datetime' : transactions.datetime,
                 'money' : transactions.money,
                 'balance' : transactions.balance,
               }
