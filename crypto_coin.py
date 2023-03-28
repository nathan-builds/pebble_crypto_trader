'''
The coin class contains all the details about each coin that is being traded
it will be used to determine when a coin should be bought and sold based on the
paramters for the individual currency
'''


class CryptoCoin:
    def __init__(self, type, buy_threshold, sell_threshold, max_pos, amount_per_trade, baseline_price=None):
        self.type = type
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        self.max_pos = max_pos
        self.amount_per_trade = amount_per_trade
        self.baseline_price = baseline_price

    def update_baseline_price(self, price):
        self.baseline_price = price
