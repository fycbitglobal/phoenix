# app/monitoring/trade_logger.py
import csv
from datetime import datetime
from app.core.logger import logger

class TradeLogger:
    def __init__(self, filename="logs/trade_history.csv"):
        self.filename = filename
        # Dosya yoksa başlıkları oluştur
        with open(self.filename, 'a', newline='') as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(["Timestamp", "Symbol", "Side", "Entry", "Exit", "Quantity", "PNL"])

    def log_trade(self, trade_data: dict):
        """Bir işlemi CSV dosyasına kaydeder."""
        try:
            with open(self.filename, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now(),
                    trade_data['symbol'],
                    trade_data['side'],
                    trade_data['entry'],
                    trade_data.get('exit', 'N/A'),
                    trade_data['qty'],
                    trade_data.get('pnl', 'N/A')
                ])
        except Exception as e:
            logger.error(f"Trade loglama hatası: {e}")
