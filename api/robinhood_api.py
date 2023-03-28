import pandas as pd
from api.market_api import MarketAPI
import robin_stocks.robinhood as rs
from datetime import datetime
from pebble_logger import PebbleLogger
from constants.base_constants import Constants
import time
import sys
from threading import Timer
from threads.exit_notification import ExitNotification
import os


class RobinhoodAPI(MarketAPI):
    '''
    This is the API that uses robin-stocks library to interact with robinhood. On a failed buy or sell order the program
    will quit to protect data integrity and avoid orphan orders
    '''

    p_log = PebbleLogger("RobinhoodAPI", True, True, 'logs/pebble_logs.log')
    logger = p_log.get_logger()

    def __init__(self):
        self.pwd = "ENVIRONMENT_PWD"
        self.user = "ENVIRONMENT_USER"
        self.last_login = None
        self.login()
        self.max_attempts = 5
        self.order_start_date = self.get_start_date()  # THIS WILL CHANGE ON RESTART OF THE BOT

    def get_start_date(self):
        '''
        API does time at UTC-5:00, format the date correctly
        @return:
        '''
        date = datetime(2022, 1, 6, 1).isoformat()
        date_string = date + '-05:00'
        utc_formatted_date = datetime.fromisoformat(date_string)
        return utc_formatted_date

    def login(self):
        try:
            rs.login(username=self.user, password=self.pwd, expiresIn=86400, by_sms=True)
            self.last_login = datetime.now()
        except Exception:
            self.logger.error("ERROR AUTHENTICATING WITH ROBINHOOD API, SHUTTING DOWN")
            print(" WE GOT HERE IN ROBINHOOD_API, DID WE SHUT DOWN?")
            os._exit()

    def place_sell_crypto_order(self, name, quantity, limit_price):
        self.login()
        attempts = 0
        sell_order = rs.orders.order_sell_crypto_limit(name, quantity, limit_price)
        time.sleep(1.0)
        order_status = self.check_order_status(sell_order)
        if order_status == Constants.FAILED:
            while order_status == Constants.FAILED and attempts <= self.max_attempts:
                sell_order = rs.orders.order_sell_crypto_limit(name, quantity, limit_price)
                time.sleep(1.0)
                order_status = self.check_order_status(sell_order)
                attempts += 1
        if order_status == Constants.SUCCESS:
            self.logger.info(
                f"SELL_ORDER - {name} - QUANTITY: {quantity} - LIMIT_PRICE: ${limit_price}")
            return sell_order
        elif order_status == Constants.FAILED:
            self.logger.error(
                f"A sell order has failed with the coin type {name}, quantity {quantity}, and limit price of {limit_price}")
            os._exit()

    def place_buy_crypto_order(self, name, dollar_amount):
        self.login()
        attempts = 0
        buy_order = rs.orders.order_buy_crypto_by_price(name, dollar_amount, timeInForce='gtc')
        time.sleep(1.0)
        order_status = self.check_order_status(buy_order)
        if order_status == Constants.FAILED:
            while order_status == Constants.FAILED and attempts <= self.max_attempts:
                buy_order = rs.orders.order_buy_crypto_by_price(name, dollar_amount, timeInForce='gtc')
                time.sleep(1.0)
                order_status = self.check_order_status(buy_order)
                attempts += 1
        if order_status == Constants.SUCCESS:
            self.logger.info(f"BUY_ORDER - {name} - DOLLAR_AMOUNT - ${dollar_amount}")
        elif order_status == Constants.FAILED:
            self.logger.error(
                f"A buy order has failed with the coin type {name}, and dollar amount of {dollar_amount}")
            os._exit()

    def get_current_crypto_price(self, ticker):
        self.login()
        price_quote = rs.get_crypto_quote(ticker)
        return float(price_quote['ask_price'])

    def get_all_orders(self):
        '''
        All orders that are past the start date of the bot. We dont care about the practice orders I was doing.
        @return:
        '''
        for i in range(1, self.max_attempts):
            print(f" ATTEMPT NUMBER {i} TO GET ORDERS")
            try:
                self.login()
                all_orders = rs.get_all_crypto_orders()
                filtered_orders = []
                for order in all_orders:
                    order_date_iso = order['created_at']
                    date = datetime.fromisoformat(order_date_iso)
                    if date > self.order_start_date:
                        filtered_orders.append(order)
                return filtered_orders
            except Exception as e:
                print(f"CAUGHT EXCEPTION IN ORDER AREA, ATTEMPTED TO EXIT,  ATTEMPT NUMBER{i}")
                print(e)
                time.sleep(1.0)

        print("ORDER FAILED, NOW EXITING")
        os._exit(-1)

    def get_crypto_id(self, name):
        self.login()
        return rs.crypto.get_crypto_id(name)

    def get_available_funds(self):
        self.login()
        investment_profile = rs.profiles.load_account_profile()
        return float(investment_profile['crypto_buying_power'])

    def check_login_time(self):
        now = datetime.now()
        difference = now - self.last_login
        if difference.seconds > 86000:  # login expires every 86400 seconds
            self.login()

    def check_order_status(self, order):
        '''
        Orders that fail have a dict length of 1
        @param order:
        @return:
        '''
        if len(order) <= Constants.FAILED_LENGTH:
            print(order)
            return Constants.FAILED
        else:
            return Constants.SUCCESS

    def get_price_24hr_ago(self, ticker):
        '''
        Get the last 24 price points, the first position is roughly 24 hrs ago
        @param ticker: Name of coin as string
        @return:
        '''
        self.login()
        last_24_price_points = rs.get_crypto_historicals(ticker, interval='hour', span='day')
        time_24hrs_ago = last_24_price_points[0]['begins_at']
        self.logger.info(f"TIME 24HRS AGO: {time_24hrs_ago}")
        return float(last_24_price_points[0]['close_price'])

    # def test_exit(self):
    #     t = Timer(10, self.exit)
    #     t.start()
    #
    # def exit(self):
    #     print("exit triggered!")
    #     os._exit(0)
