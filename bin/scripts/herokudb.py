import os
import sys
import transaction

from sqlalchemy import engine_from_config

from ..models.models import (
    DBSession,
    Base,
    UserAccount,
    OwnerBankaccount,
    Transaction,
    Costumer,
    Forum,
    BankAccount,
    RepeatPayment,
    )

def main(argv=sys.argv):
    settings = {'sqlalchemy.url': os.environ['DATABASE_URL']}
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        modelcostumer = Costumer(nationid = '1001', fullname = 'admin eieigum', brithday = datetime.datetime.now(), address = 'guy u u u u u u', phonenumber = '098765434312')
        DBSession.add(modelcostumer)
        modelaccount = BankAccount(accountname = 'adminnaja', Costumer_id = 1)
        DBSession.add(modelaccount)
        modeluser = UserAccount(username='admin', password = hash_password('1234'),role = 'editor', Costumer_id = 1)
        DBSession.add(modeluser)
        modelob   = OwnerBankaccount(userid = 1, bankid = 1)
        DBSession.add(modelob)
        modelsforum = Forum(title='root', detail='root', createdtime = datetime.datetime.now())
        DBSession.add(modelsforum)

        modelcostumer = Costumer(nationid = '0', fullname = 'government', brithday = datetime.datetime.now(), address = 'on the world', phonenumber = '0000000000')
        DBSession.add(modelcostumer)
        modelaccount = BankAccount(accountname = 'government', Costumer_id = 2)
        DBSession.add(modelaccount)
        modeluser = UserAccount(username='topsecert', password = hash_password('topsecert'), role = 'veiwer', Costumer_id = 2)
        DBSession.add(modeluser)
        modelob = OwnerBankaccount(userid = 2, bankid = 2)
        DBSession.add(modelob)


if __name__ == '__main__':
    main()
