import uuid
from decimal import Decimal

from .meta import (Amount, attribute_mapped_collection, Base, Column, GUID,
                   many_to_one, one_to_many, Session, String, SurrogatePK,
                   UniqueMixin)


class Account(UniqueMixin, SurrogatePK, Base):
    __tablename__ = 'account'

    username = Column(String(20), unique=True, nullable=False)
    balances = one_to_many(
        "AccountBalance",
        collection_class=attribute_mapped_collection("balance_type"),
        backref="account",
        lazy="immediate"
    )

    @classmethod
    def unique_hash(cls, username):
        return username

    @classmethod
    def unique_filter(cls, query, username):
        return query.filter(cls.username == username)

    def __init__(self, username):
        self.username = username

    def add_transaction(self, client, type_, amount):
        balance_type = BalanceType.as_unique(Session(), type_)

        if balance_type in self.balances:
            account_balance = self.balances[balance_type]
        else:
            account_balance = self.balances[balance_type] = \
                AccountBalance(balance_type=balance_type)

        trans = Transaction(
            account_balance=account_balance,
            amount=amount,
            client=client
        )
        Session.add(trans)
        account_balance.last_trans_id = trans.trans_id
        account_balance.balance += amount
        if account_balance.balance < Decimal("0"):
            raise ValueError("overdraft occurred")
        return trans


class AccountBalance(SurrogatePK, Base):
    __tablename__ = 'account_balance'

    balance = Column(Amount)
    last_trans_id = Column(GUID())

    balance_type = many_to_one("BalanceType", lazy="joined", innerjoin=True)
    transactions = one_to_many("Transaction", backref="account_balance")

    def __init__(self, **kw):
        self.balance = Decimal("0")
        super(AccountBalance, self).__init__(**kw)


class Transaction(SurrogatePK, Base):
    __tablename__ = 'transaction'

    trans_id = Column(GUID(), nullable=False, unique=True)
    amount = Column(Amount, nullable=False)

    client = many_to_one("Client")

    def __init__(self, **kw):
        self.trans_id = uuid.uuid4()
        super(Transaction, self).__init__(**kw)


class BalanceType(UniqueMixin, SurrogatePK, Base):
    __tablename__ = 'balance_type'

    name = Column(String(50), nullable=False)

    @classmethod
    def unique_hash(cls, name):
        return name

    @classmethod
    def unique_filter(cls, query, name):
        return query.filter(cls.name == name)

    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return other.name == self.name
