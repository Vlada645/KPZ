from datetime import datetime
from pandas import DataFrame
import pandas as pd
from os.path import exists

# Назва файлу для CSV
filename = 'timestamp_log.csv'

# Колонки для DataFrame
columns = ['year', 'month', 'day', 'hour', 'minute', 'second']

# Отримуємо поточний час
now = datetime.now()
new_row = {
    'year': now.year,
    'month': now.month,
    'day': now.day,
    'hour': now.hour,
    'minute': now.minute,
    'second': now.second
}

# Якщо файл існує — читаємо його, інакше створюємо новий DataFrame
if exists(filename):
    dataframe = pd.read_csv(filename)
    dataframe = dataframe[columns]  # гарантуємо правильний порядок
else:
    dataframe = DataFrame(columns=columns)

# Додаємо новий рядок
dataframe.loc[len(dataframe)] = new_row

# Зберігаємо у CSV
dataframe.to_csv(filename, index=False)

print("Новий запис додано до CSV.")
