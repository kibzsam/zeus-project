import ccxt
import config
import pandas as pd
import time
import schedule
import utility as u
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
timeframe = '15m'
sd_limit = 200
sd_sma = 20


def supply_demand_bot(sd_limit=sd_limit, sd_sma=sd_sma):
    # Get the OHCLV data
    # Get 4hr, 1hr, 30min, 15min, 5min OHCLV data

    # 5min
    df_5m = u.df_sma(symbol, '5m', sd_limit, sd_sma)
    # get support and resistance
    support_5m = df_5m.iloc[-1]["support"]
    resistance_5m = df_5m.iloc[-1]["resistance"]
    df_5m['support_low'] = df_5m[:-2]['low'].min()
    support_low_5m = df_5m.iloc[-1]['support_low']
    print(
        f'This is support low {support_low_5m} and this is support {support_5m} Demand Zone is between the two')

    df_5m['resistance_high'] = df_5m[:-2]['high'].max()
    resistance_high_5m = df_5m.iloc[-1]['resistance_high']
    print(
        f'This is the resistance high {resistance_high_5m} and this is resistance {resistance_5m} Supply Zone is between the two')
    time.sleep(2)

    # 15min
    df_15m = u.df_sma(symbol, '15m', sd_limit, sd_sma)
    # get support and resistance
    support_15m = df_15m.iloc[-1]["support"]
    resistance_15m = df_15m.iloc[-1]["resistance"]
    df_15m['support_low'] = df_15m[:-2]['low'].min()
    support_low_15m = df_15m.iloc[-1]['support_low']
    print(
        f'This is support low {support_low_15m} and this is support {support_15m} Demand Zone is between the two')

    df_15m['resistance_high'] = df_15m[:-2]['high'].max()
    resistance_high_15m = df_15m.iloc[-1]['resistance_high']
    print(
        f'This is the resistance high {resistance_high_15m} and this is resistance {resistance_15m} Supply Zone is between the two')
    time.sleep(2)

    # 30min
    df_30m = u.df_sma(symbol, '30m', sd_limit, sd_sma)
    # get support and resistance
    support_30m = df_30m.iloc[-1]["support"]
    resistance_30m = df_30m.iloc[-1]["resistance"]
    df_30m['support_low'] = df_30m[:-2]['low'].min()
    support_low_30m = df_30m.iloc[-1]['support_low']
    print(
        f'This is support low {support_low_30m} and this is support {support_30m} Demand Zone is between the two')

    df_30m['resistance_high'] = df_30m[:-2]['high'].max()
    resistance_high_30m = df_30m.iloc[-1]['resistance_high']
    print(
        f'This is the resistance high {resistance_high_30m} and this is resistance {resistance_30m} Supply Zone is between the two')
    time.sleep(2)

    # 1hr
    df_1h = u.df_sma(symbol, '1h', sd_limit, sd_sma)
    # get support and resistance
    support_1h = df_1h.iloc[-1]["support"]
    resistance_1h = df_1h.iloc[-1]["resistance"]
    df_1h['support_low'] = df_1h[:-2]['low'].min()
    support_low_1h = df_1h.iloc[-1]['support_low']
    print(
        f'This is support low {support_low_1h} and this is support {support_1h} Demand Zone is between the two')

    df_1h['resistance_high'] = df_1h[:-2]['high'].max()
    resistance_high_1h = df_1h.iloc[-1]['resistance_high']
    print(
        f'This is the resistance high {resistance_high_1h} and this is resistance {resistance_1h} Supply Zone is between the two')
    time.sleep(2)

    # 4hr
    df_4h = u.df_sma(symbol, '4h', sd_limit, sd_sma)
    # get support and resistance
    support_4h = df_4h.iloc[-1]["support"]
    resistance_4h = df_4h.iloc[-1]["resistance"]
    df_4h['support_low'] = df_4h[:-2]['low'].min()
    support_low_4h = df_4h.iloc[-1]['support_low']
    print(
        f'This is support low {support_low_4h} and this is support {support_4h} Demand Zone is between the two')

    df_4h['resistance_high'] = df_4h[:-2]['high'].max()
    resistance_high_4h = df_4h.iloc[-1]['resistance_high']
    print(
        f'This is the resistance high {resistance_high_4h} and this is resistance {resistance_4h} Supply Zone is between the two')
    time.sleep(2)

    # Daily
    df_1d = u.df_sma(symbol, '1d', sd_limit, sd_sma)
    # get support and resistance
    support_1d = df_1d.iloc[-1]["support"]
    resistance_1d = df_1d.iloc[-1]["resistance"]
    df_1d['support_low'] = df_1d[:-2]['low'].min()
    support_low_1d = df_1d.iloc[-1]['support_low']
    print(
        f'This is support low {support_low_1d} and this is support {support_1d} Demand Zone is between the two')

    df_1d['resistance_high'] = df_1d[:-2]['high'].max()
    resistance_high_1d = df_1d.iloc[-1]['resistance_high']
    print(
        f'This is the resistance high {resistance_high_1d} and this is resistance {resistance_1d} Supply Zone is between the two')
    # supply and demand are where the wicks of support and resistance
    # GET THE WICKS, the wicks are the highs and lows ...
    # demand zone is between the support and the support on low
    # figure out where price moves big up/down
    # and create supply and demand zones
    # output the supply and demand zones


supply_demand_bot()
