import os
import sys
import transaction
import datetime

from sqlalchemy import engine_from_config
from .encrypt import hash_password

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


if __name__ == '__main__':
    main()
