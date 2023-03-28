'''
Update wil be the object that carries information based on a time interval
Can have a type of COIN_PRICE_UPDATE or BASE_COIN_PRICE_UPDATE
'''


class Update:
    def __init__(self):
        self.list_of_coin_updates = []
        self.update_type = None
        self.test_text = ""

    # coin will be a String name here
    def add_coin_and_price(self, coin, price, update_type=None):
        coin_data = (coin, price)
        self.list_of_coin_updates.append(coin_data)
        self.update_type = update_type

    def set_test_field(self, text):
        self.test_text = text
