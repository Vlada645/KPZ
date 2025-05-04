import numpy as np
from typing import List

class Backtester:
    def __init__(self, strategy: 'Strategy'):
        self.strategy = strategy
        self.signals: List['Signal'] = []
        self.total_profit: float = 0.0

    def run(self, iterations: int = 100):
        for _ in range(iterations):
            data = self.strategy.generate_fake_data()
            signal = self.strategy.create_signal(data)
            if signal:
                result = self._simulate_trade(signal)
                signal.result = result
                self.signals.append(signal)
                self.total_profit += result

    def _simulate_trade(self, signal: 'Signal') -> float:
        multiplier = np.random.uniform(0.95, 1.05)
        final_price = signal.entry * multiplier

        if signal.side == "BUY":
            if final_price >= signal.take_profit:
                return signal.take_profit - signal.entry
            elif final_price <= signal.stop_loss:
                return signal.stop_loss - signal.entry
        elif signal.side == "SELL":
            if final_price <= signal.take_profit:
                return signal.entry - signal.take_profit
            elif final_price >= signal.stop_loss:
                return signal.entry - signal.stop_loss

        return 0.0

    def summary(self):
        print(f"Total signals: {len(self.signals)}")
        print(f"Total profit: {round(self.total_profit, 2)}")
