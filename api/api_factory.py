from api.robinhood_api import RobinhoodAPI
from api.test_api import TestAPI


class APIFactory:
    def get_market_api(api_name):
        """

        @param api_name: The name of the market API being used.
        @return: returns a instance of market_api
        Right now robinhood is the api, but in the future a different api
        may be used in its place. This will abstract the market implementation away from the
        trading logic.
        """

        if (api_name == "ROBINHOOD"):
            return RobinhoodAPI()
        elif (api_name == "TEST_API"):
            return TestAPI()
        else:
            print("API IS NOT CURRENTLY SUPPORTED")
        # add more apis here if it changes

    def __init__(self):
        pass
