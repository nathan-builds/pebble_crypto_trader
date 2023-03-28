

'''
A transaction has two components, a buy and a sell
the buy always initiates the beginning of a transaction. 
'''


class Transaction:
    def __init__(self, position):
        self.transaction_id = position.unique_id
        self.date_bought = position.buy_time
        self.coin_amount = position.coin_amount
        self.buy_price = position.buy_price
        self.date_sold = None
        self.sell_price = None

    def add_sale(self, position):
        self.date_sold = position.sell_time
        self.sell_price = position.sell_time

    def add_buy(self, position):
        self.date_bought = position.buy_time
        self.coin_amount = position.coin_amount
        self.buy_price = position.buy_price
