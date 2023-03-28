import math_helpers
import crypto_coin
from update import Update
from crypto_coin import CryptoCoin as coin
from database.transaction import Transaction
from api.api_factory import APIFactory
from constants.base_constants import Constants
from order import Order
from database.db_writer import DBWriter
import sys
import queue
from threading import Timer
import logging
from pebble_logger import PebbleLogger


class Trader:
    p_log = PebbleLogger("OrderEval", False, True, 'logs/pebble_logs_order_eval.log')
    order_eval_logger = p_log.get_logger()

    def __init__(self, account):
        self.last_update = None
        self.crypto_ids = {}  # structure = { "ja2312334kj3k2k": "ETH"}
        self.active_coins_map = {}  # structure = {"ETH": crypto_coin)}
        self.account = account
        self.db_writer = DBWriter()
        self.market_api = APIFactory.get_market_api(Constants.ROBINHOOD)
        self.list_of_transactions = []  # keep all the database transactions in memory here
        self.logger = self.get_logger()
        self.base_percent_message = ""

    def get_logger(self):
        p_log = PebbleLogger("Trader", True, True, 'logs/pebble_logs.log')
        logger = p_log.get_logger()
        return logger

    def add_coin(self, crypto_coin):
        '''
        Add the crypto coin to the actively traded list of coins
        @param crypto_coin:
        @return:
        '''
        if crypto_coin.type not in self.active_coins_map:
            self.active_coins_map[crypto_coin.type] = crypto_coin
        else:
            print("ERROR DUPLICATE COIN")

    def load_trader_data(self):
        self.load_transactions()
        self.load_crypto_ids()
        self.trigger_order_evaluation()  # evaluate all orders on startup

    def load_crypto_ids(self):
        '''
        Each cryto has a uniqe ID on Robinhood, this ID is the only way to associate a particular coin with an order
        store the ID's in a dictionary
        @return:
        '''
        for coin_name in self.active_coins_map:
            id = self.market_api.get_crypto_id(coin_name)
            self.crypto_ids[id] = coin_name

    def load_transactions(self):
        '''
        This method loads all the transactions from the database
        @return:
        '''
        self.list_of_transactions = self.db_writer.load_all_transactions()

    def process_time_update(self, update):
        '''
        Updating baseline prices is done to evaluate buy positions. For instance if at time(0) if the baseline_price=4000
        the new coin prices that come in will be evaluated against the baseline_price of 4000. So if the  new coin price
        that comes in is 3900 and it meets buy criteria it will be bought. At t(1) the baseline price will be updated
        and the new current prices will be compared against this new baseline.
        @param update: Update object containing the coinName and the new price associated with
        @return:
        '''
        if update.update_type == Constants.BASELINE:
            self.update_baseline_coin_prices(update)
        elif update.update_type == Constants.BUY_CHECK:
            for coin_name, coin_price in update.list_of_coin_updates:
                self.check_for_new_positions(coin_name, coin_price)
        self.log_update(update)

    def place_buy_order(self, coin):
        '''
        Check if there are enough available funds to buy. If there are more funds than the amount we are buying per
        coin trade then place the buy. For example if there are $90 available and each ETH buy is $5 we can make a buy
        @param coin: CryptoCoin object
        @return:
        '''
        available_funds = self.market_api.get_available_funds()
        dollar_amount_to_buy = coin.amount_per_trade
        if available_funds > dollar_amount_to_buy:
            self.market_api.place_buy_crypto_order(coin.type, dollar_amount_to_buy)

    def place_sell_order(self, order):
        '''
        Each sell order is created from an associated buy order. The sell order needs to sell the exact quantity of
        coins purchased in the buy order at a % profit that has been determined. Create a limit_order here that will
        be pending until the limit_price is reached by the market
        @param order: A buy Order object
        @return: returns a sell Order object
        '''

        coin_type = order.crypto_coin_type
        crypto_coin = self.active_coins_map.get(coin_type)
        crypto_coin_sell_threshold = crypto_coin.sell_threshold
        crypto_coin_buy_price = order.average_price
        # limit_price = math_helpers.calculate_limit_price(crypto_coin_buy_price, crypto_coin_sell_threshold)
        limit_price = self.get_limit_price(coin_type, crypto_coin_buy_price, crypto_coin_sell_threshold)
        coin_quantity = order.quantity
        sell_order = self.market_api.place_sell_crypto_order(coin_type, coin_quantity, limit_price)
        sell_order_obj = Order(sell_order, self.crypto_ids)
        return sell_order_obj

    def get_limit_price(self, coin_type, crypto_coin_buy_price, default_crypto_coin_sell_threshold):
        crypto_coin_threshold = default_crypto_coin_sell_threshold
        price_24hrs_ago = self.market_api.get_price_24hr_ago(coin_type)
        current_price = self.market_api.get_current_crypto_price(coin_type)
        price_change_24hrs = math_helpers.calculate_percentage_change(current_price, price_24hrs_ago)

        if price_change_24hrs < -9:
            crypto_coin_threshold = 5
        elif price_change_24hrs < -7:
            crypto_coin_threshold = 4
        elif price_change_24hrs < -5:
            crypto_coin_threshold = 3

        limit_price = math_helpers.calculate_limit_price(crypto_coin_buy_price, crypto_coin_threshold)
        self.logger.info(f"24HR PERCENT CHANGE: {price_change_24hrs} - LIMIT PRICE PERCENT: {crypto_coin_threshold}")
        return limit_price

    def evaluate_buy_rules(self, coin, current_coin_price):
        '''
        Method evaluates the coin current coin price against the baseline to determine if its time to place a buy order
        @param coin: the CryptoCoin object
        @param current_coin_price: current price of the coin
        @return:
        '''
        percent_change = math_helpers.calculate_percentage_change(current_coin_price, coin.baseline_price)
        self.base_percent_message = f"{coin.type} - BASE_PRICE: ${coin.baseline_price} - CURRENT_PRICE: ${current_coin_price} - PERCENT_CHANGE: {percent_change}%"
        # coin has gone down past what the buy threshold is, buy it
        if percent_change <= coin.buy_threshold:
            self.place_buy_order(coin)

    def update_baseline_coin_prices(self, update):
        '''

        @param update: Object containing the update prices of the coin
        @return:
        '''
        for coin_name, new_coin_price in update.list_of_coin_updates:
            crypto_coin = self.active_coins_map.get(coin_name)
            crypto_coin.update_baseline_price(new_coin_price)

    def check_for_new_positions(self, coin_name, current_coin_price):
        '''
        val coming in is ("ETH", $4300) for example
        account will have any coins to be traded in the coins_positions map even if there are no active positions
        @param coin_name: Name of crypto
        @param current_coin_price: price of the coin
        @return:
        '''
        crypto_coin = self.active_coins_map.get(coin_name)
        if crypto_coin:  # means coin should be traded
            self.evaluate_buy_rules(crypto_coin, current_coin_price)

    def trigger_order_evaluation(self):
        '''
        Every two minutes this function triggers an order evaluation. Is also called on initialization of Trader
        as there may be existing orders to evaluate. After evaluation timer is reset and restarted
        @return:
        '''
        self.evaluate_orders()
        order_timer = Timer(120, self.trigger_order_evaluation)  # change this time
        order_timer.start()

    def evaluate_orders(self):
        '''
        Go through all the orders to determine which ones are COMPLETED, PENDING_SALE or have NO_SALE_ORDER
        @return:
        '''
        order_list = self.market_api.get_all_orders()
        self.order_eval_logger.info(f"Order eval triggered with total number of orders: {len(order_list)}")
        for order_data in order_list:
            order = Order(order_data, self.crypto_ids)
            if order.state == Constants.FILLED:  # only matters if the order has been filled otherwise do nothing with it
                if order.side == Constants.BUY:
                    self.evaluate_buy_order(order)
                elif order.side == Constants.SELL:
                    self.evaluate_sell_order(order)

    def evaluate_buy_order(self, buy_order):
        '''
        3 scenarios exists:
        1. A transaction does not exist for this buy ID. In this case, create a new transaction from the buy order,
        write it to the database and then store it in the list of transactions
        2. The transaction exists but has no sale order associated with it. In this case, create the sale order
        and add it to the transaction entry. Write this to the database
        3. The order exists and has  state of COMPLETED. Do nothing here, this is an old order that no longer is
        relevant
        @param buy_order: The buy Order object containing all the info about the buy order.
        @return:
        '''
        transaction_exists = False
        for transaction in self.list_of_transactions:
            if transaction.buy_order_id == buy_order.order_id:  # the transaction exists, does it have a sale order?
                transaction_exists = True
                if transaction.transaction_state == Constants.NO_SELL_ORDER:
                    sell_order = self.place_sell_order(buy_order)
                    transaction.set_sell_order(sell_order)
                    self.db_writer.update_transaction()
                elif transaction.transaction_state == Constants.PENDING_SALE:
                    break
                elif transaction.transaction_state == Constants.COMPLETED:
                    break

        if not transaction_exists:
            # no transaction exists, need to create the transaction with the initial buy order
            new_transaction = Transaction()
            new_transaction.transaction_state = Constants.NO_SELL_ORDER
            new_transaction.set_buy_order(buy_order)
            self.db_writer.create_new_transaction(new_transaction)
            self.list_of_transactions.append(new_transaction)

    def evaluate_sell_order(self, sell_order):
        '''
        The only time this should be called is if the sell_order has been filled. This means that
        if a transaction exists with this sell_order and the transaction has a state of PENDING_SALE
        then it is no longer in that state. The sale has been filled so mark the transaction as complete and write
        the change to the DBase
        @param sell_order: The sell Order object
        @return:
        '''
        for transaction in self.list_of_transactions:
            if transaction.sell_order_id == sell_order.order_id:
                if transaction.transaction_state == Constants.PENDING_SALE:  # sale is no longer pending as this sale has been filled
                    transaction.sell_average_price = sell_order.average_price  # average price now that it was actually fileld
                    dollar_gain, percent_gain = self.calculate_trade_result(transaction)
                    transaction.dollar_gain = dollar_gain
                    transaction.percent_gain = percent_gain
                    transaction.sell_last_updated_at = sell_order.last_updated
                    transaction.transaction_state = Constants.COMPLETED
                    transaction.sell_state = Constants.FILLED
                    self.db_writer.update_transaction()

    def calculate_trade_result(self, transaction):
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

    def log_update(self, update):
        for coin_name, price in update.list_of_coin_updates:
            msg = f"{update.update_type} - UPDATE TRIGGERED - {coin_name} - PRICE: ${price}"
            self.logger.info(msg)
            self.logger.info(self.base_percent_message)

    # def exit_program(self):
    #     en = Exi
    #     self.account.exit_program()
