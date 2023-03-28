import requests
import time
import json
import datetime
import pandas as pd


# now = datetime.datetime.now().timestamp()
# now_milliseconds = round(now * 1000)
# print(now_milliseconds)
#
# past_date = datetime.datetime(2021, 12, 10, 9, 0, 0)
# past_date_milliseconds = round(past_date.timestamp() * 1000)
# print(past_date_milliseconds)
#
# response = requests.get(
#     f"https://api.binance.com/api/v1/klines?symbol=ETHUSDC&interval=1m&startTime={past_date_milliseconds}&endTime={now_milliseconds}")
# response_json = response.json()
# print(response_json)
#
# df = pd.DataFrame(response_json)
# df.columns = ['open_time',
#               'open', 'high', 'low', 'close', 'volume',
#               'close_time', 'qav', 'num_trades',
#               'taker_base_vol', 'taker_quote_vol', 'ignore']
#
# df.to_excel("testBinance.xls",
#             sheet_name='Sheet1',
#             na_rep='',
#             float_format=None,
#             columns=None,
#             header=True,
#             index=True,
#             index_label=None,
#             startrow=0,
#             startcol=0,
#             engine=None,
#             merge_cells=True,
#             encoding=None,
#             inf_rep='inf',
#             verbose=True,
#             freeze_panes=None,
#             storage_options=None)


def export_results(data_points):
    data_frame = pd.DataFrame(data_points, columns=['open_time', 'open', 'high', 'low', 'close', 'volume',
                                                    'close_time', 'qav', 'num_trades', 'taker_base_vol',
                                                    'taker_quote_vol', 'ignore'])
    data_frame.to_csv("btc_data_sep1_dec19_hourly.csv", header=None, index=None, sep=' ', mode='a')
    # data_frame.to_excel("eth_nov_11_18_hourly.xls",
    #                     sheet_name='Sheet1',
    #                     na_rep='',
    #                     float_format=None,
    #                     columns=None,
    #                     header=True,
    #                     index=True,
    #                     index_label=None,
    #                     startrow=0,
    #                     startcol=0,
    #                     engine=None,
    #                     merge_cells=True,
    #                     encoding=None,
    #                     inf_rep='inf',
    #                     verbose=True,
    #                     freeze_panes=None,
    #                     storage_options=None)


def get_historical_data(startDate, endDate, timeInterval, ticker):
    """

    @param startDate: yyyy/mm/dd
    @param endDate: yyyy/mm/dd
    @param timeInterval: in minutes
    @param ticker: crytpo name
    @return: final_result with all the data points for the time period
    """

    root_url = "https://api.binance.com/api/v1/klines"
    final_result = []

    s_year, s_month, s_day = startDate.split("-")
    start = datetime.datetime(int(s_year), int(s_month), int(s_day))

    e_year, e_month, e_day = endDate.split("-")
    end = datetime.datetime(int(e_year), int(e_month), int(e_day))
    num_of_calls = 0

    while start != end:
        start_period_timestamp = int(start.timestamp() * 1000)  # whatever start is in ms timestamp
        # to make time period exclusive of upper range, subtract minutes-time interval
        # 720 minutes is 12 hours, could get 720 points if interval  is 1minute, max allowed is 1000
        end_period = start + datetime.timedelta(minutes=720 - int(timeInterval))
        end_period_timestamp = int(end_period.timestamp() * 1000)
        query_string = f"{root_url}?symbol={ticker}&interval={timeInterval}h&startTime={start_period_timestamp}&endTime={end_period_timestamp}&limit=1000"

        response = requests.get(query_string)
        json = response.json()
        # go through each point and put a readable date then add it to result
        for data_point in json:
            data_point[0] = datetime.datetime.fromtimestamp(data_point[0] / 1000).strftime("%m/%d/%y, %H:%M:%S")
            data_point[6] = datetime.datetime.fromtimestamp(data_point[6] / 1000).strftime("%m/%d/%y, %H:%M:%S")
            final_result.append(data_point)

        start += datetime.timedelta(minutes=720)  # increment start to new start point
        # give api break after 5 calls
        if num_of_calls == 5:
            time.sleep(1)
            num_of_calls = 0
        else:
            num_of_calls += 1
    return final_result


results = get_historical_data("2021-09-01", "2021-12-19", "1", "BTCUSDC")
export_results(results)
