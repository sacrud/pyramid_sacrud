from .meta import SurrogatePK, Base, Column, String, BcryptType, \
            Session, utcnow, many_to_one
from sqlalchemy.orm import exc
import os
import datetime
from .account import Account

class Client(SurrogatePK, Base):
    __tablename__ = 'client'

    identifier = Column(String(32), unique=True)
    secret = Column(BcryptType)

class AuthSession(SurrogatePK, Base):
    __tablename__ = 'auth_session'

    token = Column(String(64), nullable=False)

    client = many_to_one("Client")
    account = many_to_one("Account")

    def __init__(self, client, account):
        self.client = client
        self.account = account
        self.token = self._gen_token()

    @classmethod
    def _gen_token(cls):
        return "".join("%.2x" % ord(x) for x in os.urandom(32))

    @classmethod
    def validate_token(cls, auth_token):
        try:
            return Session.query(cls).\
                        filter_by(token=auth_token).\
                        filter(AuthSession.created_at > utcnow() -
                                datetime.timedelta(seconds=360)).one()
        except exc.NoResultFound:
            return None

    @classmethod
    def create(cls, identifier, secret, account_name):
        try:
            client = Session.query(Client).filter_by(identifier=identifier).one()
        except exc.NoResultFound:
            return None
        else:
            if client.secret != secret:
                return None

        account = Account.as_unique(Session(), account_name)
        auth_session = AuthSession(client, account)
        Session.add(auth_session)
        return auth_session

def console(argv=None):

    def adduser():
        Session.add(Client(identifier=options.username, secret=options.password))
        Session.commit()

    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("config",
                            type=str,
                            help="config file")
    subparsers = parser.add_subparsers()
    subparser = subparsers.add_parser("adduser", help="add a new user")
    subparser.add_argument("username", help="username")
    subparser.add_argument("password", help="password")
    subparser.set_defaults(cmd=adduser)

    options = parser.parse_args(argv)

    from .meta import setup_from_file
    setup_from_file(options.config)
    options.cmd()
