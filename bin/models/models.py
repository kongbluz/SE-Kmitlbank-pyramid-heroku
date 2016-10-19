import datetime
from sqlalchemy import(
    ForeignKey,
    DateTime,
    Column,
    Integer,
    Text,
    Float,
)
from ..scripts.encrypt import hash_password

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension = ZopeTransactionExtension()))
Base = declarative_base()

class UserAccount(Base):
    __tablename__ = 'user'
    userid        = Column(Integer, primary_key = True)
    username      = Column(Text, unique = True, nullable = False)
    password      = Column(Text, nullable = False)
    role          = Column(Text, nullable = False)
    Costumer_id   = Column(Integer, ForeignKey('costumer.costumerid'), nullable = False)

    def __init__(self, username, password, Costumer_id, role):
        self.username = username
        self.password = password
        self.role     = role
        self.Costumer_id = Costumer_id

    @classmethod
    def by_id(cls, userid):
        return DBSession.query(UserAccount).filter(UserAccount.userid==userid).first()

    @classmethod
    def by_username(cls, username):
        return DBSession.query(UserAccount).filter(UserAccount.username==username).first()

class Costumer(Base):
    __tablename__ = 'costumer'
    costumerid    = Column(Integer, primary_key = True)
    nationid      = Column(Text, unique = True, nullable = False)
    fullname      = Column(Text)
    brithday      = Column(DateTime, nullable = False)
    address       = Column(Text)
    phonenummber  = Column(Text)

    def __init__(self, nationid, fullname, brithday, address, phonenumber):
        self.nationid = nationid
        self.fullname = fullname
        self.brithday = brithday
        self.address  = address
        self.phonenumber = phonenumber

class BankAccount(Base):
    __tablename__ = 'Bank'
    accountid     = Column(Integer, primary_key = True)
    accountname   = Column(Text, nullable = False)
    balance       = Column(Float, nullable = False)
    loan          = Column(Float, nullable = False)
    Costumer_id   = Column(Integer, ForeignKey('costumer.costumerid'), nullable = False)

    def __init__(self, accountname, Costumer_id):
        self.accountname = accountname
        self.Costumer_id = Costumer_id
        self.balance          = 5000
        self.loan             = 0

class Transaction(Base):
    __tablename__ = 'Transaction'
    transactionid     = Column(Integer, primary_key = True)
    BankAccount_id = Column(Integer, ForeignKey('Bank.accountid'))
    datetime   = Column(Text, nullable = False)
    types      = Column(Text, nullable = False)
    money      = Column(Float, nullable = False)
    balance    = Column(Float, nullable = False)
    detail     = Column(Text)

    def __init__(self, BankAccount_id, datetime, types, money, balance, detail):
        self.BankAccount_id = BankAccount_id
        self.datetime       = datetime
        self.types          = types
        self.money          = money
        self.balance        = balance
        self.detail         = detail

class OwnerBankaccount(Base):
    __tablename__ = 'OwnerBank'
    obid       = Column(Integer, primary_key = True)
    otppassword      = Column(Text)
    UserAccount_id   = Column(Integer, ForeignKey('user.userid'))
    BankAccount_id   = Column(Integer, ForeignKey('Bank.accountid'))

    def __init__(self, userid, bankid):
        self.UserAccount_id = userid
        self.BankAccount_id = bankid

class Forum(Base):
    __tablename__ = 'forum'
    ifd           = Column(Integer, primary_key= True)
    title         = Column(Text, nullable = False)
    detail        = Column(Text)
    createdtime   = Column(DateTime)

    def __init__(self, title, detail, createdtime):
        self.title = title
        self.detail = detail
        self.createdtime = createdtime
