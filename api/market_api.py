from abc import abstractmethod


class MarketAPI:

    def __init__(self):
        self.account = None

    def set_account(self, account):
        '''
        Need reference to account right now to terminate program properly
        @param account:
        @return:
        '''
        self.account = account

    @abstractmethod
    def place_sell_crypto_order(self, name, quantity, limit_price):
        pass

    @abstractmethod
    def place_buy_crypto_order(self, name, dollar_amount):
        pass

    @abstractmethod
    def get_current_crypto_price(self, ticker):
        pass

    @abstractmethod
    def get_all_orders(self):
        pass

    @abstractmethod
    def get_crypto_id(self, name):
        pass

    @abstractmethod
    def get_available_funds(self):
        pass

    @abstractmethod
    def get_price_24hr_ago(self,ticker):
        pass