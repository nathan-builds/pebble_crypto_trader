import robin_stocks.robinhood as rs
import pandas as pd
from datetime import datetime, timedelta
import pytz

rs.login(username="ENVIRONMENT_USER", password="ENVIRONMENT_PWD", expiresIn=86400, by_sms=True)

# eth_data = rs.stocks.get_stock_historicals("VOO", interval="hour", span="3month")
# (pd.DataFrame.from_dict(eth_data).to_excel
#  ("eth_15_sec_24hr.xls",
#   sheet_name='Sheet1',
#   na_rep='',
#   float_format=None,
#   columns=None,
#   header=True,
#   index=True,
#   index_label=None,
#   startrow=0,
#   startcol=0,
#   engine=None,
#   merge_cells=True,
#   encoding=None,
#   inf_rep='inf',
#   verbose=True,
#   freeze_panes=None,
#   storage_options=None))

# pd.DataFrame.from_dict(eth_data).to_csv("voo_data.csv",header=None, index=None, sep=' ', mode='a')
# '76637d50-c702-4ed1-bcb5-5b0732a81f48'


last_prices = rs.get_crypto_historicals("ETH", interval='hour', span='week')

o_d = datetime.fromisoformat('2021-12-27T14:10:29.484741-05:00')
t = o_d.tzinfo
now = datetime.now().isoformat()
now = now + '-05:00'
now = datetime.fromisoformat(now)
if now > o_d:
    print("YES")
print("test")

acc_details = rs.profiles.load_account_profile()
inv_details = rs.profiles.load_account_profile()
port_details = rs.profiles.load_portfolio_profile()
price = rs.get_crypto_quote("BTC")
orders = rs.get_all_crypto_orders()
id = rs.crypto.get_crypto_id("BTC")
order_id = orders[0]['id']
info = rs.get_crypto_order_info(order_id)
pairs = rs.get_crypto_currency_pairs()
opne_orders = rs.orders.get_all_open_crypto_orders()
positions = rs.crypto.get_crypto_positions()
prof = rs.crypto.load_crypto_profile()

result = rs.orders.order_buy_crypto_by_price("ETH", timeInForce='gtc')
print("done")
print("done")
# sell = rs.orders.order_sell_crypto_limit("ETHHHHH", .000243, 3975.00)
# if len(sell) == 1:
#     print("HERE")

# sell = rs.orders.order_sell_crypto_by_quantity("ETHHH", .000244)
print("Done")
