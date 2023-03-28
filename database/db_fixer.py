from database.transaction import Transaction
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql
from sqlalchemy_utils import database_exists, create_database
from database.transaction import Base
from testing.test_orders import TestOrderGenerator
from sqlalchemy.exc import SQLAlchemyError
import logging
from pebble_logger import PebbleLogger
from constants.base_constants import Constants
from api.robinhood_api import RobinhoodAPI
from order import Order
import math_helpers


class Fixer():

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        '''
        Establish a connection with the database. Create a new database if its the first startup and no database exists
        @return:
        '''
        try:
            engine = create_engine('mysql+pymysql://root:Password123@localhost:3333/pebble_live_v2')
            if not database_exists(engine.url):
                create_database(engine.url)
            Session = sessionmaker(bind=engine)
            self.session = Session()
            Base.metadata.create_all(engine)
        except SQLAlchemyError as e:
            self.log_database_error(e)

    def load_all_transactions(self):
        '''
        Get all existing transactions from the database
        @return:
        '''
        transactions = []
        try:
            transactions = self.session.query(Transaction).all()
        except SQLAlchemyError as e:
            self.session.rollback()

        return transactions

    def commit_changes(self):
        self.session.commit()

    def create_new_transaction(self, transaction):
        '''
        Creates a new transaction in the database
        @param transaction:
        @return:
        '''
        try:
            self.session.add(transaction)
            self.commit_changes()
        except SQLAlchemyError as e:
            self.session.rollback()


api = RobinhoodAPI()
fixer = Fixer()
orders = api.get_all_orders()
last_order = orders[0]
order_obj = Order(last_order)
order_obj.set_crypto_coin_type('ETH')
new_transaction = Transaction()
new_transaction.transaction_state = Constants.NO_SELL_ORDER
new_transaction.set_buy_order(order_obj)
fixer.create_new_transaction(new_transaction)


# transactions = fixer.load_all_transactions()


def calculate_trade_result(transaction):
    '''
    Calculates the percent gain and the dollar gain on the trade
    @param transaction: Transaction with a buy and sell order completed
    @return:
    '''
    buy_order_price = transaction.buy_average_price
    sell_order_price = transaction.sell_average_price
    coin_quantity = transaction.buy_quantity
    dollar_gain = math_helpers.calculate_gain_on_trade(buy_order_price, sell_order_price, coin_quantity)
    percent_gain = math_helpers.calculate_percentage_change(sell_order_price, buy_order_price)
    return dollar_gain, percent_gain

# for transaction in transactions:
#     if transaction.transaction_state == Constants.COMPLETED:
#         dollar_gain, percent_gain = calculate_trade_result(transaction)
#         transaction.dollar_gain = dollar_gain
#         transaction.percent_gain = percent_gain
#         fixer.commit_changes()
