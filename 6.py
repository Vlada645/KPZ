import pandas as pd
import matplotlib.pyplot as plt
from binance import Client
from datetime import datetime, timedelta
def fetch_ohlcv(symbol: str) -> pd.DataFrame:
    client = Client()
    now = datetime.utcnow()
    yesterday = now - timedelta(days=1)
    raw = client.get_historical_klines(
        symbol,
        Client.KLINE_INTERVAL_1MINUTE,
        yesterday.strftime("%Y-%m-%d %H:%M:%S"),
        now.strftime("%Y-%m-%d %H:%M:%S")
    )
    
    columns = [
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_volume', 'num_trades',
        'taker_buy_base', 'taker_buy_quote', 'ignore'
    ] 
    df = pd.DataFrame(raw, columns=columns)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['close'] = df['close'].astype(float)
    
    return df

def append_rsi(df: pd.DataFrame, window_sizes: list) -> pd.DataFrame:
    for window in window_sizes:
        change = df['close'].diff()
        ups = change.clip(lower=0).rolling(window=window).mean()
        downs = -change.clip(upper=0).rolling(window=window).mean()
        downs.replace(0, float('nan'), inplace=True)
        rs = ups / downs
        df[f'RSI_{window}'] = 100 - 100 / (1 + rs)
    return df

def plot_rsi(df: pd.DataFrame, periods: list) -> None:
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    chart_styles = ['plot', 'scatter', 'bar']
    
    for idx, (per, ax, style) in enumerate(zip(periods, axes, chart_styles)):
        values = df[f'RSI_{per}']
        if style == 'plot':
            ax.plot(df['timestamp'], values)
        elif style == 'scatter':
            ax.scatter(df['timestamp'], values, s=5)
        elif style == 'bar':
            ax.bar(df['timestamp'], values, width=0.001)
        ax.set_title(f'{style} - RSI {per}')
        ax.set_ylabel('RSI')
    
    axes[-1].set_xlabel('Time')
    plt.tight_layout()
    plt.savefig('rsi_visualization.png')
    plt.show()

if __name__ == "__main__":
    symbol = "BTCUSDT"
    rsi_periods = [14, 27, 100]
    
    data = fetch_ohlcv(symbol)
    data = append_rsi(data, rsi_periods)
    
    result_df = data[['timestamp', 'open', 'close'] + [f'RSI_{p}' for p in rsi_periods]]
    plot_rsi(result_df, rsi_periods)
