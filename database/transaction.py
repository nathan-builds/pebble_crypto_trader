from sqlalchemy import Column, String, Integer, Date, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from constants.base_constants import Constants

Base = declarative_base()


class Transaction(Base):
    '''
    Represents the table Transaction in the database
    '''
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_state = Column(String(20))

    buy_order_id = Column(String(100))
    buy_created_at = Column(DateTime)
    buy_average_price = Column(Float)
    buy_quantity = Column(Float)
    buy_type = Column(String(20))
    buy_state = Column(String(20))
    buy_last_updated_at = Column(DateTime)

    sell_order_id = Column(String(100))
    sell_created_at = Column(DateTime)
    sell_limit_price = Column(Float)
    sell_average_price = Column(Float)
    sell_quantity = Column(Float)
    sell_type = Column(String(20))
    sell_state = Column(String(20))
    sell_last_updated_at = Column(DateTime)

    dollar_gain = Column(Float)
    percent_gain = Column(Float)
    coin_type = Column(String(10))

    def __init__(self):
        pass

    def set_buy_order(self, order):
        self.buy_order_id = order.order_id
        self.buy_created_at = order.created_at
        self.buy_average_price = order.average_price
        self.buy_quantity = order.quantity
        self.buy_type = order.type
        self.buy_state = order.state
        self.buy_last_updated_at = order.last_updated
        self.coin_type = order.crypto_coin_type
        self.transaction_state = Constants.NO_SELL_ORDER  # initially buy order has no sale order

    def get_buy_order(self, order):
        pass

    def set_sell_order(self, order):
        self.sell_order_id = order.order_id
        self.sell_created_at = order.created_at
        self.sell_limit_price = order.price
        self.sell_average_price = 0  # this will be added when its actually sold at a certain price
        self.sell_quantity = order.quantity
        self.sell_type = order.type
        self.sell_state = order.state
        self.sell_last_updated_at = order.last_updated
        self.transaction_state = Constants.PENDING_SALE  # mark as pending as soon as a sale is set on the transaction

    def get_sell_order(self, order):
        pass
