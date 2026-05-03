from typing import Optional

class RSIMomentumStrategy:
    def __init__(self, period: int = 14, overbought: int = 70, oversold: int = 30):
        self.period = period
        self.overbought = overbought
        self.oversold = oversold

    async def on_candle(self, candle: dict) -> Optional[dict]:
        rsi = candle.get("rsi")

        if rsi is None:
            return None

        symbol = candle.get("symbol")

        if rsi < self.oversold:
            return {
                "symbol": symbol,
                "signal": "BUY",
                "confidence": 0.7,
                "strategy": "RSI_MOMENTUM"
            }

        elif rsi > self.overbought:
            return {
                "symbol": symbol,
                "signal": "SELL",
                "confidence": 0.7,
                "strategy": "RSI_MOMENTUM"
            }

        return None