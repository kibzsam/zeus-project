import config
import ccxt


def calculate_supply_demand_zones(exchange, symbol):
    """
    Calculates the supply and demand zones for a given symbol.

    Args:
      exchange: A ccxt.Exchange instance.
      symbol: The symbol to calculate the zones for.

    Returns:
      A tuple of (supply_zone, demand_zone).
    """

    # Get the current market data.
    market_data = exchange.fetch_ohlcv(symbol, timeframe="1h")
    print(market_data[0][2])
    # Calculate the supply and demand zones.
    supply_zone = market_data[0][2]
    demand_zone = market_data[-1][2]

    return supply_zone, demand_zone


def place_trade(exchange, symbol, side, quantity, price):
    """
    Places a trade on a given exchange.

    Args:
      exchange: A ccxt.Exchange instance.
      symbol: The symbol to trade.
      side: The side of the trade ('buy' or 'sell').
      quantity: The quantity of the asset to trade.
      price: The price to trade at.

    Returns:
      A ccxt.Order instance.
    """

    # Place the trade.
    order = exchange.create_order(symbol, side, quantity, price)

    return order


def main():
    # Create a Phemex account and API key.
    exchange = ccxt.phemex({
        'apiKey': config.ID,
        'secret': config.SECRET,
        'enableRateLimit': True
    })
    # Define the supply and demand zones.
    supply_zone, demand_zone = calculate_supply_demand_zones(
        exchange, "BTCUSD")

    # Define a loop that polls the market data and executes trades when the conditions are met.
    while True:
        # Get the current market data.
        market_data = exchange.fetch_ohlcv("BTCUSD", timeframe="1h")

        # Check if the current price is in the supply zone.
        if market_data[-1][4] <= supply_zone:
            # Place a buy order.
            order = place_trade(exchange, "BTCUSD", "buy",
                                1, market_data[-1][4])

        # Check if the current price is in the demand zone.
        if market_data[-1][4] >= demand_zone:
            # Place a sell order.
            order = place_trade(exchange, "BTCUSD", "sell",
                                1, market_data[-1][4])


if __name__ == "__main__":
    main()
