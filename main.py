import requests
import time
from account import Account
import json
from update import Update
import concurrent.futures
from manager import Manager
from threads.coin_thread import CoinThread
import os
import queue
from threads.exit_notification import ExitNotification

if __name__ == "__main__":
    manager = Manager()
    try:
        file = open("config.json")
        active_accounts = []
        json_account_data = json.load(file)
        account = Account('logs/transactions_eth.xls')

        manager.initialize_account(account, json_account_data)
        manager.start()

    except SystemExit:
        print("SYSTEM EXIT CAUGHT, NOW CLOSING THREADS")
        manager.process_shutdown()

# while running:
#        item = main_queue.get()
#        if isinstance(item, ExitNotification):
#            manager.stop_thread()
#            print("PROGRAM HAS EXITED")
#            running = False
