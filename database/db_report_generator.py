import pymysql
import pandas
import math_helpers
import robin_stocks.robinhood as rs
from datetime import datetime


class RobinhoodApiForReports:
    def login(self):
        rs.login(username="ENVIRONMENT_USER", password="ENVIRONMENT_PWD", expiresIn=86400, by_sms=True)

    def get_current_crypto_price(self, ticker):
        self.login()
        price_quote = rs.get_crypto_quote(ticker)
        return float(price_quote['ask_price'])


def get_data_frame():
    conn = pymysql.connect(host='127.0.0.1', user='root', port=3333, password='Password123', db='pebble_live_v2')
    query = "SELECT * FROM TRANSACTION"
    df = pandas.read_sql(query, conn)
    return df


def add_percent_difference_list(df):
    percent_dif_list = []
    api = RobinhoodApiForReports()

    for key, val in df.iterrows():
        coin_type = val['coin_type']
        buy_price = val['buy_average_price']  # old
        current_price = api.get_current_crypto_price(coin_type)  # new
        percent_change = math_helpers.calculate_percentage_change(current_price, buy_price)
        percent_dif_list.append(percent_change)
    df['percent_change'] = percent_dif_list


def add_days_held_list(df):
    days_held_list = []
    for key, val in df.iterrows():
        bought_at_str = str(val['buy_last_updated_at'])
        bought_at = datetime.strptime(bought_at_str, '%Y-%m-%d %H:%M:%S')

        if val['transaction_state'] == 'COMPLETED':
            sold_at_str = str(val['sell_last_updated_at'])
            sold_at = datetime.strptime(sold_at_str, '%Y-%m-%d %H:%M:%S')
            days_held = (sold_at - bought_at).days
        else:
            current_date = datetime.now()
            days_held = (current_date - bought_at).days
        days_held_list.append(days_held)
    df['days_held'] = days_held_list


def write_df_to_excel():
    df = get_data_frame()
    add_percent_difference_list(df)
    add_days_held_list(df)
    df.to_excel("pebble_record_2022-03-05.xls")


write_df_to_excel()
