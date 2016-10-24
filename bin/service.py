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
            return { 'status' : 'False',
                     'detail' : 'do not have some attribute'
                   }
        if accountfrom == accountdes :
            return { 'status' : 'False',
                     'detail' : 'do not send to same username'
                   }

        user = DBSession.query(UserAccount).filter(UserAccount.username == username).first()
        if user is None :
            return { 'status' : 'False',
                     'detail' : 'do not have this username'
                   }
        owner = DBSession.query(OwnerBankaccount).filter(OwnerBankaccount.BankAccount_id == accountfrom).filter(OwnerBankaccount.UserAccount_id == user.userid).first()
        if owner is None :
            return { 'status' : 'False',
                     'detail' : 'wrong bank account'
                   }

        bankto = DBSession.query(BankAccount).filter(BankAccount.accountid == accountdes).first()
        if bankto is None :
            return { 'status' : 'False',
                     'detail' : 'wrong destination account'
                   }

        bank = DBSession.query(BankAccount).filter(BankAccount.accountid == owner.BankAccount_id).first()
        if owner.otppassword != otp :
            return { 'status' : 'False',
                     'detail' : 'Wrong otp password'
                   }
        try:
            money = float(money)
        except Exception:
            return { 'status' : 'False',
                     'detail' : 'not money type'
                   }
        if money < 0 :
            return { 'status' : 'False',
                     'detail' : 'not money type'
                   }
        elif bank.balance - money < 0 :
            return { 'status' : 'False',
                     'detail' : 'do not have money enough'
                   }

        bank.balance -= money
        DBSession.add(Transaction(BankAccount_id = bank.accountid, datetime = datetime.datetime.now(),
                                  types = 'Online Shopping-', money = money, balance = bank.balance, detail = 'to '+bankto.accountname))

        bankto.balance += money
        DBSession.add(Transaction(BankAccount_id = bankto.accountid, datetime = datetime.datetime.now(),
                                  types = 'Online Shopping+', money = money, balance = bankto.balance, detail = 'from '+bank.accountname))
        owner.otppassword = None
        return { 'status' : 'True',
                 'detail' : 'Succes to Shopping'
               }
