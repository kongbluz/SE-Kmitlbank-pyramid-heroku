from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
    Everyone,
    Authenticated,
    )

from .models.models import DBSession, UserAccount, BankAccount, Costumer, OwnerBankaccount, Transaction
from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config
    )
import datetime
from .scripts.genOTP import GETOTP


class ProfileVeiw(object):
    def __init__(self, request):
        self.request = request
        self.logged_in = authenticated_userid(self.request)
        renderer = get_renderer("templates/profile/profile_layout.pt")
        self.layout = renderer.implementation().macros['layout']


    @view_config(route_name='profile',permission = 'viewprofile', renderer='templates/profile/online.pt')
    def profile(self):
        request = self.request
        allaccountid = DBSession.query(OwnerBankaccount).filter(OwnerBankaccount.UserAccount_id == UserAccount.by_id(self.logged_in).userid).order_by(OwnerBankaccount.BankAccount_id)
        accountid = ''
        costumer = DBSession.query(Costumer).filter(Costumer.costumerid == UserAccount.by_id(self.logged_in).Costumer_id).first()
        name     = costumer.fullname
        accountname = ''
        balance  = ''
        loan     = ''
        otppassword = None
        if 'form.submitted' in request.params :
            accountid    = request.params['selector']
        if accountid is not '':
            bank        = DBSession.query(BankAccount).filter(BankAccount.accountid == accountid).first()
            if bank is not None:
                accountname = bank.accountname
                balance     = bank.balance
                loan        = bank.loan
        else:
            accountid = ''

        ownaccount = DBSession.query(OwnerBankaccount).filter(OwnerBankaccount.UserAccount_id == accountid).first()
        if ownaccount is None :
            otppassword = None
        else :
            otppassword = ownaccount.otppassword

        if 'OTP.submitted' in request.params :
            accountid  = request.params['hiddenaccountid']
            bank        = DBSession.query(BankAccount).filter(BankAccount.accountid == accountid).first()
            accountname = bank.accountname
            balance  = bank.balance
            loan     = bank.loan
            ownaccount.otppassword = GETOTP()
            otppassword = ownaccount.otppassword
            return dict(title = 'Profile', name = name, accountname = accountname, otppassword = otppassword,
                        balance = balance, loan = loan, allaccountid = allaccountid, accountid = accountid,
                        url = request.application_url + '/profile'
                        )


        return dict(title = 'Profile', name = name, accountname = accountname, otppassword = otppassword,
                    balance = balance, loan = loan, allaccountid = allaccountid, accountid = accountid,
                    url = request.application_url + '/profile'
                    )

    @view_config(route_name='transfer',permission = 'viewprofile', renderer='templates/profile/transfer.pt')
    def tranfer(self):
        request = self.request
        allaccountid = DBSession.query(OwnerBankaccount).filter(OwnerBankaccount.UserAccount_id == UserAccount.by_id(self.logged_in).userid).order_by(OwnerBankaccount.BankAccount_id)
        accountid = ''
        balance  = ''
        message  = ''
        if 'form.submitted' in request.params :
            accountid    = request.params['selector']
        if accountid is not '':
            bank        = DBSession.query(BankAccount).filter(BankAccount.accountid == accountid).first()
            if bank is not None:
                balance     = bank.balance
        else:
            accountid = ''

        if 'transfer.submitted' in request.params :
            selectbank = request.params['selectbank']
            otheraccount = request.params['tranferaccount']
            money        = request.params['money']
            accountid    = request.params['myaccount']
            balance      = request.params['mybalance']
            if accountid is '' :
                message = 'Please select bank account'
                return dict(title = 'Transfer', message = message, allaccountid = allaccountid, accountid = accountid, balance = balance)
            if selectbank != 'KMITLbank' :
                message = 'Please select KMITL Bank'
                return dict(title = 'Transfer', message = message, allaccountid = allaccountid, accountid = accountid, balance = balance)

            otherbankaccount = DBSession.query(BankAccount).filter(BankAccount.accountid == otheraccount).first()

            if otherbankaccount is None :
                message = 'Wrong BankAccount'
                return dict(title = 'Transfer', message = message, allaccountid = allaccountid, accountid = accountid, balance = balance)

            if otherbankaccount.accountid == int(accountid) :
                message = 'can''t transfer to own accountid '
                return dict(title = 'Transfer', message = message, allaccountid = allaccountid, accountid = accountid, balance = balance)

            try:
                money =  float(money)
            except Exception as e:
                message = 'itn''t money'
                return dict(title = 'Transfer', message = message, allaccountid = allaccountid, accountid = accountid, balance = balance)

            if money < 0 :
                message = 'You don''t have negative money'
                return dict(title = 'Transfer', message = message, allaccountid = allaccountid, accountid = accountid, balance = balance)

            bank        = DBSession.query(BankAccount).filter(BankAccount.accountid == accountid).first()
            if bank.balance - money < 0 :
                message = 'You don''t have money enough'
                return dict(title = 'Transfer', message = message, allaccountid = allaccountid, accountid = accountid, balance = balance)

            bank.balance -= money
            DBSession.add(Transaction(BankAccount_id = bank.accountid, datetime = datetime.datetime.now(),
                                      types = 'Transfer', money = money, balance = bank.balance, detail = 'to '+otherbankaccount.accountname))

            otherbankaccount.balance += money
            DBSession.add(Transaction(BankAccount_id = otherbankaccount.accountid, datetime = datetime.datetime.now(),
                                      types = 'Receive', money = money, balance = otherbankaccount.balance, detail = 'from '+bank.accountname))

            message = 'Successfully transfer'
            return dict(title = 'Transfer', message = message, allaccountid = allaccountid, accountid = accountid, balance = bank.balance)

        return dict(title = 'Transfer', message = message, allaccountid = allaccountid, accountid = accountid, balance = balance)

    @view_config(route_name='loan', renderer='templates/profile/loan.pt')
    def loan(self):
        allaccountid = DBSession.query(OwnerBankaccount).filter(OwnerBankaccount.UserAccount_id == UserAccount.by_id(self.logged_in).userid).order_by(OwnerBankaccount.BankAccount_id)
        return dict(title = 'Loan', allaccountid = allaccountid)

    @view_config(route_name='transaction',permission = 'viewprofile', renderer='templates/profile/transaction.pt')
    def transaction(self):
        request = self.request
        allaccountid = DBSession.query(OwnerBankaccount).filter(OwnerBankaccount.UserAccount_id == UserAccount.by_id(self.logged_in).userid).order_by(OwnerBankaccount.BankAccount_id)
        alltransaction = None
        accountid = None
        if 'form.submitted' in request.params :
            accountid    = request.params['selector']
        if accountid is not '':
            bank        = DBSession.query(BankAccount).filter(BankAccount.accountid == accountid).first()
            if bank is not None:
                alltransaction = DBSession.query(Transaction).filter(Transaction.BankAccount_id == bank.accountid).order_by(Transaction.datetime.desc())
        else:
            accountid = ''

        return dict(title = 'Transaction', allaccountid = allaccountid, alltransaction = alltransaction)

    @view_config(route_name='autopay',permission = 'viewprofile', renderer='templates/profile/autopay.pt')
    def autopay(self):
        request = self.request
        allaccountid = DBSession.query(OwnerBankaccount).filter(OwnerBankaccount.UserAccount_id == UserAccount.by_id(self.logged_in).userid).order_by(OwnerBankaccount.BankAccount_id)
        message = None
        balance = None
        accountid = None
        if 'form.submitted' in request.params :
            accountid    = request.params['selector']
            bank        = DBSession.query(BankAccount).filter(BankAccount.accountid == accountid).first()
            balance     = bank.balance
        return dict(title = 'Auto Pay', allaccountid = allaccountid, message = message, balance = balance, accountid = accountid)
