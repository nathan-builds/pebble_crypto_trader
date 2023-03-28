from timer import UpdateTimer
import threading
from api.market_api import MarketAPI
from threading import Timer
from threads.worker_thread import WorkerThread
from update import Update
from constants.base_constants import Constants
import logging


class CoinThread(WorkerThread):
    logger = logging.getLogger("CoinThreadLogger")
    logger.setLevel(logging.INFO)
    stream = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s - %(message)s')
    stream.setFormatter(formatter)
    logger.addHandler(stream)

    def __init__(
            self,
            manager,
            coin_name,
            coin_api_ticker,
            baseline_interval,
            buy_check_interval,
            market_api):
        super().__init__()
        self.manager = manager
        self.name = coin_name
        self.coin_api_ticker = coin_api_ticker
        self.baseline_interval = baseline_interval
        self.buy_check_interval = buy_check_interval
        self.market_api = market_api
        self.baseline_timer = None
        self.price_check_timer = None
        self.set_timers()

    def run(self):
        self.start_timers()
        self.log_start()
        while True:
            item = self.task_queue.get()
            self.do_pending_work(item)

    def start_timers(self):
        '''
        Start the timers for the first time
        '''
        self.baseline_timer.start()
        self.price_check_timer.start()

    def set_timers(self):
        '''
        Sets the time parameters for each timer
        '''
        self.baseline_timer = Timer(self.baseline_interval, self.trigger_baseline_update)
        self.price_check_timer = Timer(self.buy_check_interval, self.trigger_buy_check_update)

    def restart_baseline_timer(self):
        self.baseline_timer = Timer(self.baseline_interval, self.trigger_baseline_update)
        self.baseline_timer.start()

    def restart_buy_check_timer(self):
        self.price_check_timer = Timer(self.buy_check_interval, self.trigger_buy_check_update)
        self.price_check_timer.start()

    def trigger_baseline_update(self):
        '''
        method gets fired when the baseline timer expires
        '''
        current_price = self.market_api.get_current_crypto_price(self.coin_api_ticker)
        update = Update()
        # the name is the coin name ex: "ETH"
        update.add_coin_and_price(self.name, current_price, Constants.BASELINE)
        #self.logger.info(f"Baseline update triggered for {self.name}")
        self.add_update_to_queue(update)
        self.restart_baseline_timer()

    def trigger_buy_check_update(self):
        '''
        method gets fired when the price check timer expires
        '''
        current_price = self.market_api.get_current_crypto_price(self.coin_api_ticker)
        update = Update()
        # the name is the coin name ex: "ETH"
        update.add_coin_and_price(self.name, current_price, Constants.BUY_CHECK)
        #self.logger.info(f"BuyCheck update triggered for {self.name}")
        self.add_update_to_queue(update)
        self.restart_buy_check_timer()

    def add_update_to_queue(self, update):
        self.add_task(update)

    def do_pending_work(self, item):
        if isinstance(item, Update):
            self.manager.add_task(item)
        else:
            print("ITEM IN QUEUE IS NOT OF TYPE UPDATE IN COIN THREAD")

    def log_start(self):
        self.logger.info(f"Coin Thread for {self.name} has started. ")
