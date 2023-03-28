from datetime import datetime
from constants.base_constants import Constants


class Order():
    def __init__(self, order, crypto_ids=None):
        self.side = order['side']  # buy or sell
        self.order_id = order['id']
        self.created_at = datetime.fromisoformat(order['created_at'])
        self.quantity = float(order['quantity'])
        self.type = order['type']  # market, limit etc..
        self.last_updated = datetime.fromisoformat(order['updated_at'])
        self.state = order['state']
        self.price = float(order['price'])  # always a price associated with the order

        if self.state == Constants.FILLED:
            # if order filled there is a average_price it was performed at
            self.average_price = float(order['average_price'])

        if crypto_ids:
            self.crypto_coin_type = self.determine_coin_type(crypto_ids, order)

    def determine_coin_type(self, crypto_ids, order):
        '''
        Determine what coin is associated with this order. For example did we buy BTC or ETH or something else
        @param crypto_ids: Dictionary of crypto ids {"hd32234-djsc4j": "ETH"}
        @param order: Order object
        @return:
        '''
        crypto_order_id = order['currency_pair_id']
        crypto_coin_type = crypto_ids.get(crypto_order_id)
        return crypto_coin_type

    def set_crypto_coin_type(self, type):
        self.crypto_coin_type = type
