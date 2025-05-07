import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

# === Генерація випадкових даних ===
np.random.seed(42)
n = 300
price = np.cumsum(np.random.randn(n)) + 100
df = pd.DataFrame({'close': price})
df['open'] = df['close'].shift(1).bfill()  # оновлено: використовує bfill()
df['high'] = df[['open', 'close']].max(axis=1) + np.random.rand(n)
df['low'] = df[['open', 'close']].min(axis=1) - np.random.rand(n)
df.index = pd.date_range(start='2024-01-01', periods=n)

# === Розрахунок індикаторів ===
df['ema_short'] = EMAIndicator(close=df['close'], window=10).ema_indicator()
df['ema_long'] = EMAIndicator(close=df['close'], window=50).ema_indicator()
df['ema_trend'] = EMAIndicator(close=df['close'], window=200).ema_indicator()
df['rsi'] = RSIIndicator(close=df['close'], window=14).rsi()

# === Умови входу ===
df['long'] = (
    (df['ema_short'] > df['ema_long']) &
    (df['ema_short'].shift(1) <= df['ema_long'].shift(1)) &
    (df['rsi'] < 30) &
    (df['close'] > df['ema_trend'])
)

df['short'] = (
    (df['ema_short'] < df['ema_long']) &
    (df['ema_short'].shift(1) >= df['ema_long'].shift(1)) &
    (df['rsi'] > 70) &
    (df['close'] < df['ema_trend'])
)

# === Побудова графіка ===
plt.figure(figsize=(14, 6))
plt.plot(df['close'], label='Ціна', color='gray')
plt.plot(df['ema_short'], label='EMA 10', linestyle='--', color='orange')
plt.plot(df['ema_long'], label='EMA 50', linestyle='--', color='blue')
plt.plot(df['ema_trend'], label='EMA 200', linestyle='--', color='black')

# Входи
plt.scatter(df.index[df['long']], df['close'][df['long']], marker='^', color='green', label='LONG сигнал', zorder=5)
plt.scatter(df.index[df['short']], df['close'][df['short']], marker='v', color='red', label='SHORT сигнал', zorder=5)

plt.title('EMA + RSI Strategy (Random Data)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
