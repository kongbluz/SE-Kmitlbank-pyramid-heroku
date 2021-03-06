from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
    Everyone
    )

from .models.models import DBSession, UserAccount, BankAccount, Costumer, OwnerBankaccount, Forum
from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config
    )

import datetime
from .scripts.encrypt import check_password, hash_password
from .scripts.encrypt import encode_ba, decode_ba

class View(object):
    def __init__(self, request):
        self.request = request
        self.logged_in = authenticated_userid(self.request)
        renderer = get_renderer("templates/mainpage/index.pt")
        self.index = renderer.implementation().macros['index']

    @view_config(route_name='home', renderer='templates/mainpage/home.pt')
    @forbidden_view_config(renderer='templates/mainpage/home.pt')
    def home(self):
        request = self.request
        allnews = DBSession.query(Forum).order_by(Forum.createdtime.desc())
        login = ''
        password = ''
        message = ''

        checkrole = DBSession.query(UserAccount).filter(UserAccount.userid == self.logged_in).first()
        if checkrole is not None:
            role = checkrole.role
        else:
            role = 'viewer'

        if 'form.submitted' in request.params:
            login = request.params['login']
            password = request.params['password']
            confirm = UserAccount.by_username(login)
            if confirm is not None and check_password(password, confirm.password):
                headers = remember(request, confirm.userid)
                response = request.response
                response.headerlist.extend(headers)
                return HTTPFound( location = '/profile', headers = headers)
            else:
                message = 'username or password is invalid'
        return dict(title = 'Home', url = request.application_url + '/', login = login, password = password, message = message, allnews = allnews, role = role)

    @view_config(route_name='contact', renderer='templates/mainpage/contact.pt')
    def contact(self):
        return dict(title = 'Contact')

    @view_config(route_name='about', renderer='templates/mainpage/about.pt')
    def about(self):
        return dict(title = 'About')

    @view_config(route_name='service', renderer='templates/mainpage/service.pt')
    def service(self):
        return dict(title = 'Service')

    @view_config(route_name='success', renderer='templates/mainpage/success.pt')
    def success(self):
        request = self.request
        username = request.GET['getusername']

        return dict(title = 'Registration Success', username = username)

    @view_config(route_name='news', renderer='templates/mainpage/news.pt')
    def news(self):
        request = self.request
        ifd = int(self.request.matchdict['ifd'])
        thisnews = DBSession.query(Forum).filter(Forum.ifd == ifd).one()
        newstitle = thisnews.title
        detail = thisnews.detail
        time = thisnews.createdtime

        return dict(title = 'News', newstitle = newstitle, detail = detail, time = time)

    @view_config(route_name='register', renderer='templates/mainpage/register.pt')
    def register(self):
        request = self.request
        message = ''
        username = ''
        try:
            accountid   =  request.GET['getaccountid']
            nationid    =  request.GET['getnationid']
        except Exception:
            accountname = ''
            accountid = ''
            nationid = ''

        if 'form.submitted' in request.params:
            username    = request.params['username']
            password    = request.params['password']
            accountid   = request.params['accountid']
            nationid    = request.params['nationid']


            costumer = DBSession.query(Costumer).filter(Costumer.nationid == nationid).first()
            bankaccount = DBSession.query(BankAccount).filter(BankAccount.accountid == decode_ba(accountid)).first()

            if costumer is None :
                message = 'Wrong Nationid'
                return dict(title = 'Register', username = username, message = message, url = request.application_url + '/register', nationid = nationid, accountid = accountid)

            if bankaccount is None :
                message = 'Wrong accountid'
                return dict(title = 'Register', username = username, message = message, url = request.application_url + '/register', nationid = nationid, accountid = accountid)

            if costumer.costumerid != bankaccount.Costumer_id :
                message = 'You aren''t owner of this bankaccount '
                return dict(title = 'Register', username = username, message = message, url = request.application_url + '/register', nationid = nationid, accountid = accountid)

            if DBSession.query(UserAccount).filter(UserAccount.username == username).first() is not None :
                message = 'the username is already used '
                return dict(title = 'Register', username = username, message = message, url = request.application_url + '/register', nationid = nationid, accountid = accountid)

            DBSession.add(UserAccount(username = username, password = hash_password(password), role = 'viewer', Costumer_id = costumer.costumerid))
            account  = DBSession.query(UserAccount).filter(UserAccount.Costumer_id == costumer.costumerid).order_by(UserAccount.userid.desc()).first()
            DBSession.add(OwnerBankaccount(userid = account.userid, bankid = bankaccount.accountid))
            return HTTPFound(location = 'register/success?'+'getusername='+username)

        return dict(title = 'Register', username = username, message = message, url = request.application_url + '/register', nationid = nationid, accountid = accountid)

    @view_config(route_name='accountregister', renderer='templates/mainpage/regist-account.pt')
    def userregister(self):
        request = self.request
        message = ''
        name = ''
        nationid = ''
        brithday = ''
        address = ''
        phonenumber = ''
        url = request.application_url + '/accountregister'
        if 'form.submitted' in request.params:
            name = request.params['name']
            nationid = request.params['nationid']
            brithday = request.params['brithday']
            address = request.params['address']
            phonenumber = request.params['phonenumber']
            if brithday.find('/') != 2 :
                message = 'invalid brithday type'
                return dict(title = 'Account Register',
                            name = name,
                            message = message,
                            nationid = nationid,
                            brithday = brithday,
                            address = address,
                            url = url,
                            phonenumber = phonenumber)

            else:
                brith = brithday.split('/')

                try:
                    brithdate = datetime.date(int(brith[2]), int(brith[1]), int(brith[0]))
                except Exception:
                    message = 'invalid brithday type'
                    return dict(title = 'Account Register',
                                name = name,
                                message = message,
                                nationid = nationid,
                                brithday = brithday,
                                address = address,
                                url = url,
                                phonenumber = phonenumber)

                thiscostumerid = DBSession.query(Costumer).filter(Costumer.nationid == nationid).first()
                if thiscostumerid is  None :
                    DBSession.add(Costumer(nationid = nationid, fullname = name, brithday = brithdate, address = address, phonenumber = phonenumber))
                    thiscostumerid = DBSession.query(Costumer).filter(Costumer.nationid == nationid).first().costumerid
                else:
                    thiscostumerid = thiscostumerid.costumerid
                DBSession.add(BankAccount(accountname = name, Costumer_id = thiscostumerid))
                thisaccountid = DBSession.query(BankAccount).filter(BankAccount.accountname == name).filter(BankAccount.Costumer_id == thiscostumerid).order_by(BankAccount.accountid.desc()).first().accountid
                return HTTPFound( location = 'register?'+'getaccountid='+encode_ba(thisaccountid)+'&getnationid='+nationid)

        return dict(title = 'Account Register',
                    name = name,
                    message = message,
                    nationid = nationid,
                    brithday = brithday,
                    address = address,
                    url = url,
                    phonenumber = phonenumber)

    @view_config(route_name='logout')
    def logout(self):
        request = self.request
        headers = forget(request)
        url = request.route_url('home')
        return HTTPFound(location=url,
                         headers=headers)
