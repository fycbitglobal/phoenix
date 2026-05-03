# app/strategy_engine/smc/fair_value_gap.py
import pandas as pd
from app.strategy_engine.base_strategy import BaseStrategy
from app.core.types import Signal, OrderSide
from typing import Optional

class FVGStrategy(BaseStrategy):
    def __init__(self, symbols: list):
        super().__init__("SMC_FVG_Strategy", symbols)
        self.history = {symbol: [] for symbol in symbols}
        self.fvg_zones = {symbol: [] for symbol in symbols} # Aktif FVG bölgelerini tutar

    async def on_candle(self, candle: dict) -> Optional[Signal]:
        symbol = candle['symbol']
        self.history[symbol].append(candle)
        if len(self.history[symbol]) < 3: return None

        df = pd.DataFrame(self.history[symbol])
        
        # Son 3 mumu al
        c1 = df.iloc[-3] # Birinci mum
        c2 = df.iloc[-2] # İkinci mum (Impulse mum)
        c3 = df.iloc[-1] # Üçüncü mum

        # --- Bullish FVG (Yükseliş Boşluğu) ---
        # C1'in yükseği, C3'ün düşüğünden düşükse arada boşluk vardır.
        if c1['high'] < c3['low']:
            fvg_top = c3['low']
            fvg_bottom = c1['high']
            self.fvg_zones[symbol].append({"type": "BULLISH", "top": fvg_top, "bottom": fvg_bottom})
            
            return Signal(
                symbol=symbol,
                side=OrderSide.BUY,
                strength=0.6,
                strategy_name=self.name,
                metadata={"type": "FVG_BULLISH", "zone": (fvg_bottom, fvg_top)}
            )

        # --- Bearish FVG (Düşüş Boşluğu) ---
        # C1'in düşüğü, C3'ün yüksekliğinden fazlaysa arada boşluk vardır.
        if c1['low'] > c3['high']:
            fvg_top = c1['low']
            fvg_bottom = c3['high']
            self.fvg_zones[symbol].append({"type": "BEARISH", "top": fvg_top, "bottom": fvg_bottom})
            
            return Signal(
                symbol=symbol,
                side=OrderSide.SELL,
                strength=0.6,
                strategy_name=self.name,
                metadata={"type": "FVG_BEARISH", "zone": (fvg_bottom, fvg_top)}
            )

        return None
