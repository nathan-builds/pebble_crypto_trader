def calculate_percentage_change(new, old):
    return float(((new - old) / old) * 100)  # force float here for everything


def calculate_gain_on_trade(buy_price, sell_price, coin_quantity):
    dollar_gain = sell_price - buy_price
    result = float(dollar_gain * coin_quantity)
    return result


def calculate_limit_price(purchase_price, sell_threshold):
    sell_threshold = float(sell_threshold / 100)
    percent_gain = float(1 + sell_threshold)
    price_needed = float(percent_gain * purchase_price)
    return round(price_needed, 2)  # round float to two decimal places


buy_p = 3327.07
sell_p = 3393.68
coin_q = .001503
result = calculate_gain_on_trade(buy_p, sell_p, coin_q)
p_change = calculate_percentage_change(sell_p, buy_p)
