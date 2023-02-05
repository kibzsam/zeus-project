# Coding Algo Orders
# connect exchange
import ccxt
import config


phemex = ccxt.phemex({
    'apiKey': config.ID,
    'secret': config.SECRET,
    'enableRateLimit': True
})
phemex.set_sandbox_mode(True)
balance = phemex.fetch_balance()
symbol = 'uBTCUSD'
size = 1
bid = 23400
params = {'timeInForce': 'PostOnly'}

# making an order
# buyOrder = phemex.create_limit_buy_order(symbol, size, bid, params)
phemex.cancel_all_orders(symbol)
