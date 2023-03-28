import xlwt
from xlwt import Workbook
from transaction import Transaction
from datetime import datetime
import math_helpers


class Bookkeeper:
    def __init__(self, records_path, account):
        self.workbook = Workbook()

        self.account = account
        self.next_buy_row = 1
        self.next_update_row = 1
        self.next_sale_row = 1
        self.next_account_summary_row = 1
        self.file_path = records_path

        self.buy_sheet = self.workbook.add_sheet('Buy')
        self.sale_sheet = self.workbook.add_sheet('Sell')
        self.price_update_sheet = self.workbook.add_sheet('Price_Updates')
        self.account_summary_sheet = self.workbook.add_sheet("Account_Summary")
        # structure is {pos_id: (row_num, position)}
        # self.row_transaction_map = {}
        self.write_column_headers()

    def write_column_headers(self):
        self.buy_sheet.write(0, 0, "ID")
        self.buy_sheet.write(0, 1, "ACTION")
        self.buy_sheet.write(0, 2, "DATE_BOUGHT")
        self.buy_sheet.write(0, 3, "BUY_PRICE")
        self.buy_sheet.write(0, 4, "COIN_AMOUNT")

        self.sale_sheet.write(0, 0, "ID")
        self.sale_sheet.write(0, 1, "ACTION")
        self.sale_sheet.write(0, 2, "DATE_SOLD")
        self.sale_sheet.write(0, 3, "COIN_AMOUNT")
        self.sale_sheet.write(0, 4, "SALE_PRICE")
        self.sale_sheet.write(0, 5, "$GAIN/LOSS ON TRADE")
        self.sale_sheet.write(0, 6, "%GAIN/LOSS ON TRADE ")

        self.price_update_sheet.write(0, 0, "ACTION")
        self.price_update_sheet.write(0, 1, "UPDATED_PRICE")
        self.price_update_sheet.write(0, 2, "TIME")
        self.price_update_sheet.write(0, 3, "COIN")
        self.price_update_sheet.write(0, 4, "PERCENT_CHANGE")

        self.account_summary_sheet.write(0, 0, "ACTION")
        self.account_summary_sheet.write(0, 1, "TIME")
        self.account_summary_sheet.write(0, 2, "TOTAL_AVAILABLE_FUNDS")
        self.account_summary_sheet.write(0, 3, "TOTAL_ACCOUNT_VALUE")
        self.account_summary_sheet.write(0, 4, "TOTAL_ACTIVE_POSITIONS")
        self.account_summary_sheet.write(0, 5, "REALIZED_GAINS/LOSSES")
        self.account_summary_sheet.write(0, 6, "UNREALIZED_GAINS/LOSSES")

        self.workbook.save(self.file_path)

    def log_sale(self, position):
        row_num = self.next_sale_row
        percent_gain_or_loss_on_trade = math_helpers.calculate_percentage_change(position.sell_price,
                                                                                 position.buy_price)
        self.sale_sheet.write(row_num, 0, f"{position.unique_id}")
        self.sale_sheet.write(row_num, 1, "SALE")
        self.sale_sheet.write(row_num, 2, f"{position.get_readable_sell_date()}")
        self.sale_sheet.write(row_num, 3, f"{position.coin_amount}")
        self.sale_sheet.write(row_num, 4, f"{position.sell_price}")
        self.sale_sheet.write(row_num, 5, f"{position.gains_losses}")
        self.sale_sheet.write(row_num, 6, f"{percent_gain_or_loss_on_trade}")
        self.next_sale_row += 1
        self.workbook.save(self.file_path)

    def log_buy(self, position):
        row_num = self.next_buy_row
        self.buy_sheet.write(row_num, 0, f"{position.unique_id}")
        self.buy_sheet.write(row_num, 1, "BUY")
        self.buy_sheet.write(row_num, 2, f"{position.get_readable_buy_date()}")
        self.buy_sheet.write(row_num, 3, f"{position.buy_price}")
        self.buy_sheet.write(row_num, 4, f"{position.coin_amount}")
        self.next_buy_row += 1
        self.workbook.save(self.file_path)

    def log_account_update(
            self,
            action,
            total_avail_funds,
            total_acc_value,
            total_act_positions,
            realized_gl,
            unrealized_gl):
        row_num = self.next_account_summary_row
        self.account_summary_sheet.write(row_num, 0, f"{action}")
        self.account_summary_sheet.write(row_num, 1, f"{datetime.now()}")
        self.account_summary_sheet.write(row_num, 2, f"{total_avail_funds}")
        self.account_summary_sheet.write(row_num, 3, f"{total_acc_value}")
        self.account_summary_sheet.write(row_num, 4, f"{total_act_positions}")
        self.account_summary_sheet.write(row_num, 5, f"{realized_gl}")
        self.account_summary_sheet.write(row_num, 6, f"{unrealized_gl}")
        self.next_account_summary_row += 1
        self.workbook.save(self.file_path)

# def write_column_headers(self):
#     self.transaction_sheet.write(0, 0, "ID")
#     self.transaction_sheet.write(0, 1, "ACTION")
#     self.transaction_sheet.write(0, 2, "DATE_BOUGHT")
#     self.transaction_sheet.write(0, 3, "BUY_PRICE")
#     self.transaction_sheet.write(0, 4, "COIN_AMOUNT")
#     self.transaction_sheet.write(0, 5, "DATE_SOLD")
#     self.transaction_sheet.write(0, 6, "SALE_PRICE")
#     self.transaction_sheet.write(0, 7, "GAINS/LOSSES ON TRADE")
#     self.transaction_sheet.write(0, 8, "TOTAL_GAINS_LOSSES")
#     self.transaction_sheet.write(0, 9, "TOTAL_ACCOUNT_VALUE")
#
#     self.price_update_sheet.write(0, 0, "ACTION")
#     self.price_update_sheet.write(0, 1, "UPDATED_PRICE")
#     self.price_update_sheet.write(0, 2, "TIME")
#     self.price_update_sheet.write(0, 3, "COIN")
#     self.price_update_sheet.write(0, 4, "PERCENT_CHANGE")
#
#     self.workbook.save(self.file_path)
#
# def log_buy(self, position):
#     row_num = self.next_trans_row;
#     self.transaction_sheet.write(row_num, 0, f"{position.unique_id}")
#     self.transaction_sheet.write(row_num, 1, "TRANSACTION")
#     self.transaction_sheet.write(row_num, 2, f"{position.get_readable_buy_date()}")
#     self.transaction_sheet.write(row_num, 3, f"{position.buy_price}")
#     self.transaction_sheet.write(row_num, 4, f"{position.coin_amount}")
#     self.row_transaction_map[position.unique_id] = (row_num, position)
#     self.workbook.save(self.file_path)
#     self.next_trans_row += 1
#
# def log_sale(self, position):
#     row_position = self.row_transaction_map[position.unique_id]
#     row_num = row_position[0]
#     self.transaction_sheet.write(row_num, 5, f"{position.get_readable_sell_date()}")
#     self.transaction_sheet.write(row_num, 6, f"{position.sell_price}")
#     self.transaction_sheet.write(row_num, 7, f"{position.gains_losses}")
#     self.transaction_sheet.write(row_num, 8, f"{self.account.gains_losses_amount}")
#     self.transaction_sheet.write(row_num, 9, f"{self.account.total_account_value}")
#     self.workbook.save(self.file_path)
#
# def log_price_update(self, coin, new_price, old_price, type):
#     row_num = self.next_update_row
#     time = datetime.now()
#     percent_change = math_helpers.calculate_percentage_change(new_price, old_price)
#     if type == "BASELINE":
#         self.price_update_sheet.write(row_num, 0, "BASELINE_PRICE-UPDATE")
#     elif type == "COIN_UPDATE":
#         self.price_update_sheet.write(row_num, 0, "COIN_PRICE_CHANGE")
#
#     self.price_update_sheet.write(row_num, 1, f"{new_price}")
#     self.price_update_sheet.write(row_num, 2, f"{time}")
#     self.price_update_sheet.write(row_num, 3, f"{coin}")
#     self.price_update_sheet.write(row_num, 4, f"{percent_change}")
#     self.next_update_row += 1
#     self.workbook.save(self.file_path)
