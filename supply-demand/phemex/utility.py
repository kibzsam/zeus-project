import ccxt
import config
import pandas as pd
import time
import schedule


phemex = ccxt.phemex({
    'apiKey': config.ID,
    'secret': config.SECRET,
    'enableRateLimit': True
})

phemex.set_sandbox_mode(True)
balance = phemex.fetch_balance()
symbol = 'uBTCUSD'
size = 1
params = {'timeInForce': 'PostOnly'}


# making an order
# buyOrder = phemex.create_limit_buy_order(symbol, size, bid, params)
# phemex.cancel_all_orders(symbol)
# open positions
def open_positions(symbol=symbol):
    # what is the position index for that symbol?
    if symbol == 'uBTCUSD':
        index_pos = 4
    elif symbol == 'APEUSD':
        index_pos = 2
    elif symbol == 'ETHUSD':
        index_pos = 3
    elif symbol == 'DOGEUSD':
        index_pos = 1
    elif symbol == 'u100000SHIBUSD':
        index_pos = 0
    else:
        index_pos = None

    params = {'type': 'swap', 'code': 'USD'}
    phemex_bal = phemex.fetch_balance(params=params)
    open_positions = phemex_bal['info']['data']['positions']

# dictionaries
    openpos_side = open_positions[index_pos]['side']
    openpos_size = open_positions[index_pos]['size']
    # print(open_positions)

# if statements
    if openpos_side == ('Buy'):
        openpos_bool = True
        long = True
    elif openpos_side == ('Sell'):
        openpos_bool = True
        long = False
    else:
        openpos_bool = False
        long = None
    print(
        f'open_positions... | openpos_bool {openpos_bool} | openpos_size{openpos_size} | long {long} | index_pos{index_pos}')
    return open_positions, openpos_bool, openpos_size, long, index_pos

    # Kill Switch : This will be a function that you can call any moment and it will take you out of the position

# This is the ask and bid for a particular symbol: We can use this function to get the order book of a symbol and probably optimize it in future to determine buys or sell based on the order book.


def ask_bid(symbol=symbol):
    order_book = phemex.fetch_order_book(symbol)
    # print(ob)
    bid = order_book['bids'][0][0]
    ask = order_book['asks'][0][0]
    bid_liq = order_book['bids'][0][1]
    ask_liq = order_book['asks'][0][1]

    return ask, bid, order_book, bid_liq, ask_liq


def kill_switch(symbol=symbol):

    print(f'starting the kill switch for {symbol}')
    openposi = open_positions(symbol)[1]
    long = open_positions(symbol)[3]
    kill_size = open_positions(symbol)[2]

    print(f'openposi {openposi}, long{long}, size {kill_size}')

    while openposi == True:

        print('starting kill switch loop till limit fil...')
        temp_df = pd.DataFrame()
        print(f'just made a temp df {temp_df}')

        phemex.cancel_all_orders(symbol)
        openposi = open_positions(symbol)[1]
        long = open_positions(symbol)[3]
        kill_size = open_positions(symbol)[2]
        kill_size = int(kill_size)

        ask = ask_bid(symbol)[0]
        bid = ask_bid(symbol)[1]

        if long == False:
            phemex.create_limit_buy_order(symbol, kill_size, bid, params)
            print(
                f'Just made a Buy to close order of {kill_size} {symbol} at ${bid}')
            print('sleeping for 30 seconds to see it fills...')
            time.sleep(30)
        elif long == True:
            phemex.create_limit_sell_order(symbol, kill_size, ask, params)
            print(
                f'just made a SELL to CLOSE order of {kill_size} {symbol} at ${ask}')
            print('sleeping for 30 seconds to see if it fills...')
            time.sleep(30)
        else:
            print('++++++ SOMETHING I DIDNT EXCEPT IN KILL SWITCH FUNCTION')
        openposi = open_positions(symbol)[1]


# pnl close
# pnl_close() [0] pnlclose and [1] in_pos [2]size [3]long TF


def pnl_close(symbol, target, max_loss):
    print(f'checking to see if its time to exit for {symbol}...')
    params = {'type': 'swap', 'code': 'USD'}
    pos_dict = phemex.fetch_positions(params=params)
    # print(pos_dict)

    index_pos = open_positions(symbol)[4]
    pos_dict = pos_dict[index_pos]
    side = pos_dict['side']
    size = pos_dict['contracts']
    entry_price = float(pos_dict['entryPrice'])
    leverage = float(pos_dict['leverage'])

    current_price = ask_bid(symbol)[1]

    print(f'side: {side} | entry_price:{entry_price} | lev: {leverage}')
    # short or long

    if side == 'long':
        diff = current_price - entry_price
        long = True
    else:
        diff = entry_price - current_price
        long = False

# try /except
    try:
        perc = round(((diff/entry_price) * leverage), 10)
    except:
        perc = 0
    perc = 100 * perc
    print(f'for {symbol} this is our PNL percentage: {(perc)}%')

    pnlclose = False
    in_pos = False

    if perc > 0:
        in_pos = True
        print(f'for {symbol} we are in a winning position')
        if perc > target:
            print(
                ':) :) we are in profit & hit target.. checking volume to see if we should start kill switch')
            pnlclose = True
            kill_switch(symbol)
        else:
            print('we have not hit our target yet')

    elif perc < 0:
        in_pos = True

        if perc <= max_loss:
            print(
                f'we need to exit now down {perc}... so starting the kill switch.. max loss {max_loss}')
            kill_switch(symbol)
        else:
            print(
                f'we are in a losing position of {perc}..but chillen cause max loss is {max_loss}')
    else:
        print('we are not in position')

    print(f' for{symbol} just finished checking PNL close..')

    return pnlclose, in_pos, size, long


def size_kill():
    max_risk = 1000

    params = {'type': 'swap', 'code': 'USD'}
    all_phe_balance = phemex.fetch_balance(params=params)
    open_positions = all_phe_balance['info']['data']['postions']
    # print(open_positions)

    try:
        pos_cost = open_positions[0]['posCost']
        pos_cost = float(pos_cost)
        openpos_side = open_positions[0]['side']
        openpos_size = open_positions[0]['size']
    except:
        pos_cost = 0
        openpos_side = 0
        openpos_size = 0
    print(f'position cost: {pos_cost}')
    print(f'openpos_side:{openpos_side}')

    if pos_cost > max_risk:

        print(
            f'EMERGENCY KILL SWITCH ACTIVATED DUE TO CURRENT POSITION SIZE OF {pos_cost} OVER MAX RISK OF: {max_risk}')
        kill_switch(symbol)
        time.sleep(30000)
    else:
        print(
            f'size kill check: current position cost is {pos_cost} we are gucci')


# Define the timeframe  to trade the asset
# Define the bar limit:Number of bars to check the limit
# Define the sma ie 20 sma, 200 sma etc

def df_sma(symbol, timeframe, limit, sma):
    bars = phemex.fetch_ohlcv(symbol=symbol, timeframe=timeframe, limit=limit)
    df_sma = pd.DataFrame(
        bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df_sma['timestamp'] = pd.to_datetime(df_sma['timestamp'], unit='ms')

    # DAILY SMA - eg 20 day sma
    df_sma[f'sma{sma}_{timeframe}'] = df_sma.close.rolling(sma).mean()

    # if bid <  the 20 day sma then = BEARISH, if bid > 20 day sma = BULLISH

    bid = ask_bid(symbol)[1]

    # if sma > bid = SELL, if sma < bid = BUY
    df_sma.loc[df_sma[f'sma{sma}_{timeframe}'] > bid, 'sig'] = 'SELL'
    df_sma.loc[df_sma[f'sma{sma}_{timeframe}'] < bid, 'sig'] = 'BUY'

    df_sma['support'] = df_sma[:-2]['close'].min()
    df_sma['resistance'] = df_sma[:-2]['close'].max()

    df_sma['PC'] = df_sma['close'].shift(1)

    # last close Bigger than Previous close
    # going to add this to order to ensure we only open
    # order on reversal confirmation
    df_sma.loc[df_sma['close'] > df_sma['PC'], 'lcBpc'] = True
    # 2.981       > 2.966 == True
    df_sma.loc[df_sma['close'] < df_sma['PC'], 'lcBpc'] = False
    # 2.980       < 2.981 == False
    # 2.966       < 2.967 == False
    return df_sma


def position_info():
    '''
    This function gets the position info we need to trade. It switches between the positions 0 and 1 on the output
    '''
    params = {'type': 'swap', 'code': 'USD'}

    balance = phemex.fetch_balance(params=params)
    open_positions = balance['info']['data']['positions']
    pos_df = pd.DataFrame.from_dict(open_positions)
    print(pos_df)
    pos_cost = pos_df.loc[pos_df['symbol'] == symbol, 'posCost'].values[0]
    side = pos_df.loc[pos_df['symbol'] == symbol, 'side'].values[0]
    pos_cost = float(pos_cost)
    pos_size = pos_df.loc[pos_df['symbol'] == symbol, 'size'].values[0]
    size = float(pos_size)
    entryPrice = pos_df.loc[pos_df['symbol']
                            == symbol, 'avgEntryPrice'].values[0]
    entry_price = float(entryPrice)
    leverage = pos_df.loc[pos_df['symbol'] == symbol, 'leverage'].values[0]
    leverage = float(leverage)

    # print(
    #     f'symbol:{symbol} side: {side} leverage: {leverage} size{size} entry:{entry_price}')
    # post info, side,size, etry price and leverage
    return pos_cost, side, size, entry_price, leverage
