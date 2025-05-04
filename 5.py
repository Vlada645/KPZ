import pandas as pd
from binance.client import Client
from datetime import datetime, timedelta
def get_binance_client() -> Client:
    """Ініціалізація клієнта Binance."""
    return Client()
def get_time_range(days_back: int) -> tuple[str, str]:
    """Розрахунок діапазону часу."""
    now = datetime.utcnow()
    earlier = now - timedelta(days=days_back)
    return earlier.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y-%m-%d %H:%M:%S")

def load_market_data(symbol: str, interval: str, days: int = 30) -> pd.DataFrame:
    """Завантаження ринкових даних з Binance."""
    client = get_binance_client()
    start, end = get_time_range(days)
    raw_data = client.get_historical_klines(symbol, interval, start, end)
    
    df = pd.DataFrame(raw_data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_volume', 'num_trades',
        'taker_base_vol', 'taker_quote_vol', 'ignore'
    ])
    
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['close'] = df['close'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['volume'] = df['volume'].astype(float)
    
    return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]

def rsi_calc(prices: pd.Series, window: int = 14) -> pd.Series:
    delta = prices.diff()
    up = delta.clip(lower=0).rolling(window=window).mean()
    down = -delta.clip(upper=0).rolling(window=window).mean()
    rs = up / down
    return 100 - (100 / (1 + rs))

def sma_calc(prices: pd.Series, period: int) -> pd.Series:
    return prices.rolling(window=period).mean()

def bollinger_bands_calc(prices: pd.Series, period: int = 20) -> pd.DataFrame:
    sma = sma_calc(prices, period)
    std_dev = prices.rolling(window=period).std()
    upper = sma + 2 * std_dev
    lower = sma - 2 * std_dev
    return pd.DataFrame({'BBL': lower, 'BBM': sma, 'BBU': upper})

def atr_calc(high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14) -> pd.Series:
    range1 = high - low
    range2 = (high - close.shift()).abs()
    range3 = (low - close.shift()).abs()
    true_range = pd.concat([range1, range2, range3], axis=1).max(axis=1)
    return true_range.rolling(window=window).mean()

def append_indicators(data: pd.DataFrame) -> pd.DataFrame:
    data['RSI'] = rsi_calc(data['close'])
    data['SMA_50'] = sma_calc(data['close'], 50)
    data['SMA_200'] = sma_calc(data['close'], 200)
    
    bb = bollinger_bands_calc(data['close'])
    data = pd.concat([data, bb], axis=1)
    
    data['ATR'] = atr_calc(data['high'], data['low'], data['close'])
    return data

def export_csv(data: pd.DataFrame, path: str) -> None:
    data.to_csv(path, index=False)
    print(f"CSV файл збережено: {path}")

def main():
    trading_pair = "BTCUSDT"
    time_interval = Client.KLINE_INTERVAL_1HOUR
    data = load_market_data(trading_pair, time_interval)
    enriched_data = append_indicators(data)
    export_csv(enriched_data, "analysis_output.csv")
    print(enriched_data.tail())

if __name__ == "__main__":
    main()
