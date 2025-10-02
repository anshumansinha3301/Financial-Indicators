#!/usr/bin/env python3
import math
import random
from typing import List, Dict

def simple_moving_average(prices: List[float], period: int) -> List[float]:
    sma = []
    for i in range(len(prices)):
        if i + 1 < period:
            sma.append(None)
        else:
            sma.append(sum(prices[i + 1 - period:i + 1]) / period)
    return sma

def exponential_moving_average(prices: List[float], period: int) -> List[float]:
    ema = []
    k = 2 / (period + 1)
    for i, price in enumerate(prices):
        if i == 0:
            ema.append(price)
        else:
            ema.append(price * k + ema[-1] * (1 - k))
    return ema

def relative_strength_index(prices: List[float], period: int = 14) -> List[float]:
    rsi = []
    gains, losses = 0.0, 0.0
    for i in range(1, len(prices)):
        change = prices[i] - prices[i - 1]
        gains += max(0, change)
        losses += max(0, -change)
        if i >= period:
            avg_gain = gains / period
            avg_loss = losses / period
            rs = avg_gain / avg_loss if avg_loss != 0 else 0
            rsi.append(100 - 100 / (1 + rs))
            old_change = prices[i - period + 1] - prices[i - period]
            gains -= max(0, old_change)
            losses -= max(0, -old_change)
        else:
            rsi.append(None)
    rsi.insert(0, None)
    return rsi

def bollinger_bands(prices: List[float], period: int = 20, std_dev: float = 2.0) -> List[Dict[str, float]]:
    bands = []
    for i in range(len(prices)):
        if i + 1 < period:
            bands.append({"upper": None, "lower": None, "middle": None})
        else:
            window = prices[i + 1 - period:i + 1]
            mean = sum(window) / period
            variance = sum((p - mean) ** 2 for p in window) / period
            std = math.sqrt(variance)
            bands.append({"upper": mean + std_dev * std, "lower": mean - std_dev * std, "middle": mean})
    return bands

def demo():
    prices = [100 + random.uniform(-1, 1) for _ in range(50)]
    print("Prices:", [round(p,2) for p in prices])
    print("SMA(10):", [round(p,2) if p else None for p in simple_moving_average(prices, 10)])
    print("EMA(10):", [round(p,2) for p in exponential_moving_average(prices, 10)])
    print("RSI(14):", [round(p,2) if p else None for p in relative_strength_index(prices, 14)])
    bands = bollinger_bands(prices, 20)
    print("Bollinger Bands(20):")
    for b in bands:
        print({k: round(v,2) if v else None for k,v in b.items()})

if __name__ == "__main__":
    demo()
