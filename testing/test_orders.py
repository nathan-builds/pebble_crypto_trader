from order import Order
from datetime import datetime
import random
import string


class TestOrderGenerator():
    list_of_orders = []
    order_dict = {}
    crypto_ids = {}

    def __init__(self):
        self.init_dict()

    def init_dict(self):
        self.order_dict['side'] = 'buy'
        self.order_dict['id'] = 'hshd-1728392-kaksdjf-23832'
        self.order_dict['created_at'] = str(datetime.now().isoformat())
        self.order_dict['cumulative_quantity'] = "0.000243"
        self.order_dict['average_price'] = '3915.67'
        self.order_dict['type'] = 'market'
        self.order_dict['updated_at'] = str(datetime.now().isoformat())
        self.order_dict['state'] = 'filled'
        self.order_dict['currency_pair_id'] = '76637d50-c702-4ed1-bcb5-5b0732a81f48'  # ETH ID

        self.crypto_ids['76637d50-c702-4ed1-bcb5-5b0732a81f48'] = "ETH"
        self.crypto_ids['3d961844-d360-45fc-989b-f6fca761d511'] = "BTC"

    def generate_orders(self):
        order_1 = Order(self.order_dict, self.crypto_ids)
        self.list_of_orders.append(order_1)
        self.alter_order_dict()
        order_2 = Order(self.order_dict, self.crypto_ids)
        self.list_of_orders.append(order_2)
        self.alter_order_dict()
        order_3 = Order(self.order_dict, self.crypto_ids)
        self.list_of_orders.append(order_3)

        # self.order_dict['side'] = 'sell'
        # self.order_dict['id'] = 'BVXPYP534D6K9TGO5PGZ'
        # self.order_dict['type'] = 'limit'
        # self.order_dict['average_price'] = '4698.98'
        # sell_order = Order(self.order_dict, self.crypto_ids)
        # self.list_of_orders.append(sell_order)

    def alter_order_dict(self):
        id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        self.order_dict['id'] = id
        self.order_dict['created_at'] = str(datetime.now().isoformat())
        self.order_dict['cumulative_quantity'] = "0.000243"
        new_price = round(random.uniform(3900.00, 4000.00), 2)
        self.order_dict['average_price'] = new_price
        self.order_dict['updated_at'] = str(datetime.now().isoformat())
        self.order_dict['state'] = 'filled'

    def generate_random_buy_order(self, name):
        self.alter_order_dict()
        if name == "ETH":
            self.order_dict['currency_pair_id'] = '76637d50-c702-4ed1-bcb5-5b0732a81f48'
        elif name == "BTC":
            self.order_dict['currency_pair_id'] = '3d961844-d360-45fc-989b-f6fca761d511'
        order = Order(self.order_dict, self.crypto_ids)
        return order

    def generate_random_sell_order(self, name, quantity, limit_price):
        self.alter_order_dict()
        self.order_dict['average_price'] = limit_price
        self.order_dict['cumulative_quantity'] = quantity
        if name == "ETH":
            self.order_dict['currency_pair_id'] = '76637d50-c702-4ed1-bcb5-5b0732a81f48'
        elif name == "BTC":
            self.order_dict['currency_pair_id'] = '3d961844-d360-45fc-989b-f6fca761d511'
        self.order_dict['side'] = 'sell'
        sell_order = Order(self.order_dict, self.crypto_ids)
        return sell_order
