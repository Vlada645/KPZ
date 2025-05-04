import pandas as pd
from binance import Client
from datetime import datetime, timedelta

def get_binance_client() -> Client:
    """Ініціалізує клієнт Binance API."""
    return Client()

def get_time_range(days: int = 1) -> tuple:
    """Повертає часовий діапазон для запиту."""
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)
    return start_time, end_time

def fetch_klines(client: Client, symbol: str, start: datetime, end: datetime) -> list:
    """Отримує історичні свічки для символу."""
    interval = Client.KLINE_INTERVAL_1MINUTE
    start_str = start.strftime("%Y-%m-%d %H:%M:%S")
    end_str = end.strftime("%Y-%m-%d %H:%M:%S")
    return client.get_historical_klines(symbol, interval, start_str, end_str)

def prepare_dataframe(klines: list) -> pd.DataFrame:
    """Конвертує список свічок у DataFrame та обробляє типи."""
    df = pd.DataFrame(
        klines,
        columns=[
            'time', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'trades',
            'taker_buy_base', 'taker_buy_quote', 'ignore'
        ]
    )
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df['close'] = df['close'].astype(float)
    return df

def calculate_rsi_for_period(df: pd.DataFrame, period: int) -> pd.Series:
    """Розраховує RSI для заданого періоду."""
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    loss.replace(0, float('nan'), inplace=True)
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_rsi(symbol: str, periods: list) -> pd.DataFrame:
    """Основна функція для розрахунку RSI."""
    client = get_binance_client()
    start, end = get_time_range()
    klines = fetch_klines(client, symbol, start, end)
    df = prepare_dataframe(klines)

    for period in periods:
        rsi_column = f'RSI_{period}'
        df[rsi_column] = calculate_rsi_for_period(df, period)

    result_columns = ['time', 'open', 'close'] + [f'RSI_{p}' for p in periods]
    return df[result_columns]

if __name__ == "__main__":
    asset_symbol = "BTCUSDT"
    rsi_periods = [14, 27, 100]
    result = calculate_rsi(asset_symbol, rsi_periods)
    print(result)
