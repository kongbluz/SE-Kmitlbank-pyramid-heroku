import os
import sys
import transaction
import datetime

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models.models import (
    DBSession,
    Base,
    UserAccount,
    OwnerBankaccount,
    Transaction,
    Costumer,
    Forum,
    BankAccount,
    )

from .encrypt import hash_password

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
         '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
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
        modelob   = OwnerBankaccount(userid = '1', bankid = '1')
        DBSession.add(modelob)
        modelsforum = Forum(title='root', detail='root', createdtime = datetime.datetime.now())
        DBSession.add(modelsforum)
