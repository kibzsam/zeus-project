import ccxt
import time

# Define Phemex API key and secret
apikey = 'YOUR_API_KEY'
secret = 'YOUR_SECRET_KEY'

# Connect to Phemex exchange using CCXT library
exchange = ccxt.phemex({
    'apiKey': apikey,
    'secret': secret,
})

# Define function to identify supply and demand zones


def identify_zones(data):
    # Get high and low prices for the last 24 hours
    highs = data[-96:-1]['high']
    lows = data[-96:-1]['low']

    # Calculate average high and low prices
    avg_high = sum(highs) / len(highs)
    avg_low = sum(lows) / len(lows)

    # Calculate zone thresholds as a percentage of the average high and low prices
    demand_zone_threshold = 0.05
    supply_zone_threshold = 0.05

    # Calculate demand and supply zone prices
    demand_zone = avg_low - (avg_low * demand_zone_threshold)
    supply_zone = avg_high + (avg_high * supply_zone_threshold)

    return (demand_zone, supply_zone)

# Define function to buy in demand zone


def buy_in_demand_zone():
    # Get current price data
    data = exchange.fetch_ohlcv('uBTC/USD', '15m')

    # Identify supply and demand zones
    demand_zone, supply_zone = identify_zones(data)

    # Get current price
    current_price = data[-1]['close']

    # Check if current price is in demand zone
    if current_price <= demand_zone:
        # Buy uBTCUSD
        order = exchange.create_market_buy_order('uBTC/USD', 1000)
        print('Bought 1000 uBTCUSD at market price: {}'.format(
            order['average']))

    # Wait 15 minutes before checking again
    time.sleep(900)

# Define function to sell in supply zone


def sell_in_supply_zone():
    # Get current price data
    data = exchange.fetch_ohlcv('uBTC/USD', '15m')

    # Identify supply and demand zones
    demand_zone
