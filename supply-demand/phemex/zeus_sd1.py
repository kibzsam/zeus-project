import ccxt
import time

exchange = ccxt.phemex({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET',
})

symbol = 'uBTC/USD'
timeframe = '15m'


def get_supply_demand_zones(data):
    lows = data['low']
    highs = data['high']
    closes = data['close']

    highest_high = max(highs[:-1])
    lowest_low = min(lows[:-1])
    current_close = closes[-1]

    if current_close > highest_high:
        supply_zone = highest_high
        demand_zone = lowest_low
    elif current_close < lowest_low:
        supply_zone = highest_high
        demand_zone = lowest_low
    else:
        supply_zone = None
        demand_zone = None

    return supply_zone, demand_zone


def buy():
    balance = exchange.fetch_balance()
    amount = balance['uBTC']['free']
    order = exchange.create_order(symbol, type='limit', side='buy',
                                  amount=amount, price=exchange.fetch_ticker(symbol)['bid'])
    print('Bought:', order)


def sell():
    position = exchange.fetch_position(symbol)
    amount = position['size']
    order = exchange.create_order(symbol, type='limit', side='sell',
                                  amount=amount, price=exchange.fetch_ticker(symbol)['ask'])
    print('Sold:', order)


while True:
    data = exchange.fetch_ohlcv(symbol, timeframe)
    supply_zone, demand_zone = get_supply_demand_zones(data)

    if demand_zone is not None:
        buy()
    elif supply_zone is not None:
        sell()

    time.sleep(60)
