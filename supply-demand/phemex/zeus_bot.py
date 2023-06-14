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


def supply_demand(sd_limit=sd_limit, sd_sma=sd_sma, symbol=symbol):
    # Get the OHCLV data
    # Get 4hr, 1hr, 30min, 15min, 5min OHCLV data
    print('starting supply demand calculations ....')
    sd_df = pd.DataFrame()

    # 5min
    df_5m = u.df_sma(symbol, '5m', sd_limit, sd_sma)
    # get support and resistance
    support_5m = df_5m.iloc[-1]["support"]
    resistance_5m = df_5m.iloc[-1]["resistance"]
    # get support low and resistance high
    df_5m['support_low'] = df_5m[:-2]['low'].min()
    support_low_5m = df_5m.iloc[-1]['support_low']
    df_5m['resistance_high'] = df_5m[:-2]['high'].max()
    resistance_high_5m = df_5m.iloc[-1]['resistance_high']
    # get demand and supply zone 5min
    sd_df['dz_5m'] = [support_low_5m, support_5m]
    sd_df['sz_5m'] = [resistance_high_5m, resistance_5m]
    time.sleep(1)

    # 15min
    df_15m = u.df_sma(symbol, '15m', sd_limit, sd_sma)
    # get support and resistance 15min
    support_15m = df_15m.iloc[-1]["support"]
    resistance_15m = df_15m.iloc[-1]["resistance"]
    # get support low and resistance high
    df_15m['support_low'] = df_15m[:-2]['low'].min()
    support_low_15m = df_15m.iloc[-1]['support_low']
    df_15m['resistance_high'] = df_15m[:-2]['high'].max()
    resistance_high_15m = df_15m.iloc[-1]['resistance_high']
    # get demand and supply zone 15min
    sd_df['dz_15m'] = [support_low_15m, support_15m]
    sd_df['sz_15m'] = [resistance_high_15m, resistance_15m]
    time.sleep(1)

    # 30min
    df_30m = u.df_sma(symbol, '30m', sd_limit, sd_sma)
    # get support and resistance
    support_30m = df_30m.iloc[-1]["support"]
    resistance_30m = df_30m.iloc[-1]["resistance"]
    # get support low and resistance high
    df_30m['support_low'] = df_30m[:-2]['low'].min()
    support_low_30m = df_30m.iloc[-1]['support_low']
    df_30m['resistance_high'] = df_30m[:-2]['high'].max()
    resistance_high_30m = df_30m.iloc[-1]['resistance_high']
    # get demand and supply zone 15min
    sd_df['dz_30m'] = [support_low_30m, support_30m]
    sd_df['sz_30m'] = [resistance_high_30m, resistance_30m]
    time.sleep(1)

    # 1hr
    df_1h = u.df_sma(symbol, '1h', sd_limit, sd_sma)
    # get support and resistance
    support_1h = df_1h.iloc[-1]["support"]
    resistance_1h = df_1h.iloc[-1]["resistance"]
    # get support low and resistance high
    df_1h['support_low'] = df_1h[:-2]['low'].min()
    support_low_1h = df_1h.iloc[-1]['support_low']
    df_1h['resistance_high'] = df_1h[:-2]['high'].max()
    resistance_high_1h = df_1h.iloc[-1]['resistance_high']
    # get demand and supply zone 1h
    sd_df['dz_1h'] = [support_low_1h, support_1h]
    sd_df['sz_1h'] = [resistance_high_1h, resistance_1h]
    time.sleep(1)

    # 4hr
    df_4h = u.df_sma(symbol, '4h', sd_limit, sd_sma)
    # get support and resistance
    support_4h = df_4h.iloc[-1]["support"]
    resistance_4h = df_4h.iloc[-1]["resistance"]
    # get support low and resistance high
    df_4h['support_low'] = df_4h[:-2]['low'].min()
    support_low_4h = df_4h.iloc[-1]['support_low']
    df_4h['resistance_high'] = df_4h[:-2]['high'].max()
    resistance_high_4h = df_4h.iloc[-1]['resistance_high']
    # get demand and supply zone 4h
    sd_df['dz_4h'] = [support_low_4h, support_4h]
    sd_df['sz_4h'] = [resistance_high_4h, resistance_4h]
    time.sleep(1)

    # Daily
    df_1d = u.df_sma(symbol, '1d', sd_limit, sd_sma)
    # get support and resistance
    support_1d = df_1d.iloc[-1]["support"]
    resistance_1d = df_1d.iloc[-1]["resistance"]
    # get support low and resistance high
    df_1d['support_low'] = df_1d[:-2]['low'].min()
    support_low_1d = df_1d.iloc[-1]['support_low']
    df_1d['resistance_high'] = df_1d[:-2]['high'].max()
    resistance_high_1d = df_1d.iloc[-1]['resistance_high']
    # get demand and supply zone 1d
    sd_df['dz_1d'] = [support_low_1d, support_1d]
    sd_df['sz_1d'] = [resistance_high_1d, resistance_1d]
    return sd_df

    # RETURN SUPPLY AND DEMAND ZONE PER TIME FRAME

    # supply and demand are where the wicks of support and resistance
    # GET THE WICKS, the wicks are the highs and lows ...
    # demand zone is between the support and the support on low
    # figure out where price moves big up/down
    # and create supply and demand zones
    # output the supply and demand zones


def sd_bot():
    sd_df = supply_demand(symbol='uBTCUSD')
    print(sd_df)


schedule.every(5).seconds.do(sd_bot)

# Continously Run this bot
while True:
    try:
        schedule.run_pending()
        time.sleep(15)
    except:
        print('error...... sleeping 30 sec and retrying')
        time.sleep(30)
