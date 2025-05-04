import pandas as pd
import matplotlib.pyplot as plt

# Завантаження даних з CSV
data = pd.read_csv('rsi_data.csv')  # Переконайтесь, що файл знаходиться в тій самій папці
dates = pd.to_datetime(data['Date'])

# Отримання значень RSI для трьох періодів
rsi_14 = data['RSI_14']
rsi_21 = data['RSI_21']
rsi_27 = data['RSI_27']

# Створення полотна для трьох графіків
plt.figure(figsize=(9, 3))

# bar - RSI 27
plt.subplot(131)
plt.bar(dates, rsi_27)
plt.title('bar - RSI 27')

# scatter - RSI 21
plt.subplot(132)
plt.scatter(dates, rsi_21)
plt.title('scatter - RSI 21')

# plot - RSI 14
plt.subplot(133)
plt.plot(dates, rsi_14)
plt.title('plot - RSI 14')

plt.tight_layout()
plt.savefig('rsi_charts.png')  # Зберігає графік у файл
plt.show()  # Показує графіки на екрані
