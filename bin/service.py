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
from .scripts.encrypt import decode_ba

CONST_MRNONZ = "UX239I4NB1"
CONST_CESE   = "746H32ABMN"

class service(object):
    def __init__(self, request):
        self.request = request

    @view_config(route_name='trade', renderer='json')
    def trade(self):
        request = self.request
        try:
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
                     'detail' : 'do not send to same account'
                   }

        owner = DBSession.query(OwnerBankaccount).filter(OwnerBankaccount.BankAccount_id == decode_ba(accountfrom)).first()
        if owner is None :
            return { 'status' : False,
                     'detail' : 'wrong bank account'
                   }

        bankto = DBSession.query(BankAccount).filter(BankAccount.accountid == decode_ba(accountdes)).first()
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
        myaccount = DBSession.query(OwnerBankaccount).filter(OwnerBankaccount.BankAccount_id == decode_ba(account)).first()
        if myaccount is None:
            return { 'status' : False,
                     'detail' : 'wrong Bank Account'
                   }

        if myaccount.otppassword == otppassword :
            myaccount.passcodepp = GETOTP() + GETOTP()
            myaccount.otppassword = None
            bank      = DBSession.query(BankAccount).filter(BankAccount.accountid == decode_ba(account)).first()
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

        owner = DBSession.query(OwnerBankaccount).filter(OwnerBankaccount.BankAccount_id == decode_ba(accountfrom)).first()
        if owner is None :
            return { 'status' : False,
                     'detail' : 'wrong bank account'
                   }

        bankto = DBSession.query(BankAccount).filter(BankAccount.accountid == decode_ba(accountdes)).first()
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

    @view_config(route_name='checkbl', renderer='json')
    def checkbl(self):
        request = self.request
        try:
            account     = request.GET['account']
            passcode    = request.GET['passcode']
        except Exception as e:
            return { 'status' : False,
                     'detail' : 'do not have some attribute'
                   }

        ownbank = DBSession.query(OwnerBankaccount).filter(OwnerBankaccount.BankAccount_id == decode_ba(account)).first()
        if ownbank is None :
            return { 'status' : False,
                     'detail' : 'Wrong Bank account',
                   }

        if ownbank.passcodepp != passcode :
            return { 'status' : False,
                     'detail' : 'Wrong passcode'
                   }

        bank  = DBSession.query(BankAccount).filter(BankAccount.accountid == decode_ba(account)).first()
        return{ 'status' : True,
                'detail' : 'Success to checkbl',
                'balance' : bank.balance
              }

    @view_config(route_name='transfer_otbank', renderer='json', request_method='POST')
    def transfer_otbank(self):
        try:
            jsonbody = self.request.json_body
        except Exception:
            return { 'status' : False,
                     'error_message' : 'Wrong Protocal'
                   }
        try:
            accountid   = jsonbody["from_Account"]
            accounttoid = jsonbody["to_Account"]
            money    = jsonbody["Amount"]
            code     = jsonbody["key"]
        except Exception:
            return { 'status' : False,
                     'error_message' : 'Wrong attribute'
                   }
        if code == CONST_MRNONZ :
            bankname = "(MrNONZ Bank)"
        elif code == CONST_CESE :
            bankname = "(CESE Bank)"
        else :
            return { 'status' : False,
                     'error_message' : 'Wrong code'
                   }

        bankaccountto = DBSession.query(BankAccount).filter(BankAccount.accountid == decode_ba(accounttoid)).first()
        if bankaccountto is None:
            return { 'status' : False,
                     'error_message' : 'Wrong To_Bankaccount'
                   }

        bankaccountto.balance += money
        DBSession.add(Transaction(BankAccount_id = bankaccountto.accountid, datetime = datetime.datetime.now(),
                                  types = 'Receive', money = money, balance = bankaccountto.balance, detail = 'from '+accountid+' '+bankname))
        return { 'status' : True,
                 'error_message' : 'Success jaaaaa'
               }
