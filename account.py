from trader import Trader
from crypto_coin import CryptoCoin
from update import Update
from bookkeeper import Bookkeeper
from api.api_factory import APIFactory
from constants.base_constants import Constants
from pebble_logger import PebbleLogger
import sys


class Account:
    def __init__(self, log_path):
        self.trader = Trader(self)
        self.bookkeeper = Bookkeeper(log_path, self)
        self.market_api = APIFactory.get_market_api(Constants.ROBINHOOD)
        self.logger = self.get_logger()
        self.manager = None

    def get_logger(self):
        p_log = PebbleLogger("Account", True, True, 'logs/pebble_logs.log')
        logger = p_log.get_logger()
        return logger

    def process_time_update(self, update):
        '''
        At each update interval this method is called from Manager to process a update
        @param update:
        @return:
        '''
        self.trader.process_time_update(update)

    def set_account_parameters(self, config_file):
        '''
        Set all the account parameters from the inputted JSON file
        @param config_file: The trading json config file
        @return:
        '''
        for coin in config_file["coins"]:
            name = coin["coinName"]
            buy_threshold = coin['buyThreshold']
            sell_threshold = coin['sellThreshold']
            max_pos = coin['maxPos']
            coin_base_price = self.get_initial_coin_price(coin)
            amount_per_trade = coin['dollarTradeAmount']
            crypto_coin = CryptoCoin(name, buy_threshold, sell_threshold, max_pos, amount_per_trade, coin_base_price)
            self.trader.add_coin(crypto_coin)

    def load_account_trader_data(self):
        self.trader.load_trader_data()

    def get_initial_coin_price(self, coin):
        coin_api_name = coin['apiName']
        coin_price = self.market_api.get_current_crypto_price(coin_api_name)
        self.logger.info(f"INITIAL_BASE_PRICE FOR {coin_api_name} -  ${coin_price}")
        return coin_price

    def set_manager(self, manager):
        self.manager = manager

    def exit_program(self, exit_notification):
        self.manager.add_priority_task(exit_notification)
