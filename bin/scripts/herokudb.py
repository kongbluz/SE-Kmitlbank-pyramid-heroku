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

    

if __name__ == '__main__':
    main()
