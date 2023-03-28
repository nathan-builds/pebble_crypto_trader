from api.market_api import MarketAPI
import random
from testing.test_orders import TestOrderGenerator
from order import Order
from datetime import datetime


class TestAPI(MarketAPI):
    def __init__(self):
        self.test_orders = TestOrderGenerator()
        self.list_of_orders = self.test_orders.list_of_orders



    def place_sell_crypto_order(self, name, quantity, limit_price):
        sell_order = self.test_orders.generate_random_sell_order(name, quantity, limit_price)
        self.list_of_orders.append(sell_order)
        return sell_order

    def place_buy_crypto_order(self, name, dollar_amount):
        order = self.test_orders.generate_random_buy_order()
        self.list_of_orders.append(order)

    def get_current_crypto_price(self, ticker):
        if ticker == "ETH":
            return round(random.uniform(3900.00, 4000.00), 2)
        elif ticker == "BTC":
            return round(random.uniform(47000.00, 48000.00), 2)

    def get_all_orders(self):
        return self.list_of_orders

    def get_crypto_id(self, name):
        if name == "ETH":
            return '76637d50-c702-4ed1-bcb5-5b0732a81f48'
        elif name == "BTC":
            return '3d961844-d360-45fc-989b-f6fca761d511'

    def get_available_funds(self):
        return 1000
