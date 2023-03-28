from account import Account
from threads.worker_thread import WorkerThread
from threads.coin_thread import CoinThread
from api.api_factory import APIFactory
from constants.base_constants import Constants
from update import Update
from threads.exit_notification import ExitNotification


class Manager(WorkerThread):

    def __init__(self):
        super().__init__()
        self.account = None
        self.active_coin_threads = []
        self.market_api = APIFactory.get_market_api(Constants.ROBINHOOD)  # hardcoded because its the only API right now
        self.closed_orders = []

    def send_accounts_update(self, update):
        '''
        Send the update object to the trader
        @param update: Update object containing a coin and a new price
        @return:
        '''
        self.account.process_time_update(update)

    def initialize_account(self, account, account_params_file):
        '''
        Set all the account parameters. Load trader data, create the coin threads
        @param account: The trading account
        @param account_params_file: The account parameters JSON file
        @return:
        '''
        account.set_account_parameters(account_params_file)
        account.load_account_trader_data()
        account.set_manager(self)
        self.account = account
        self.create_coin_threads(account_params_file)

    def create_coin_threads(self, account_params_file):
        '''
        For each coin to be traded, create a thread with the timers associated with the coin.
        Start the thread so that at timer intervals updates will be sent to the account for each of the
        respective coins
        @param account_params_file: JSON file
        @return:
        '''
        for coin in account_params_file['coins']:
            name = coin["coinName"]
            api_ticker = coin['apiName']
            baseline_interval = coin['baselineTimer']
            price_check_interval = coin['buyCheckTimer']
            thread = CoinThread(
                self,
                name,
                api_ticker,
                baseline_interval,
                price_check_interval,
                self.market_api)
            self.active_coin_threads.append(thread)
            thread.start()

    def do_pending_work(self, item):
        if isinstance(item, Update):
            self.account.process_time_update(item)
        elif isinstance(item, ExitNotification):
            self.process_shutdown(item)
        else:
            print("ITEM IS NOT OF TYPE UPDATE OR EXIT NOTIFICATION IN THE MANAGER QUEUE")

    def process_shutdown(self):
        '''
        Close the coin threads, then alert the main thread to close
        @param exit_notification:
        @return:
        '''
        for coin_thread in self.active_coin_threads:
            coin_thread.stop_thread()
        self.stop_thread()
