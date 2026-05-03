# app/core/config.py
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# .env dosyasındaki değişkenleri yükle
load_dotenv()

class Settings(BaseSettings):
    """
    Sistem ayarlarını tutan sınıf. 
    Değerler öncelikle .env dosyasından, yoksa varsayılan değerlerden alınır.
    """
    # API Anahtarları (Boş bırakırsan hata vermez, ama gerçek işlem için doldurmalısın)
    BINANCE_API_KEY: str = os.getenv("BINANCE_API_KEY", "default_key")
    BINANCE_API_SECRET: str = os.getenv("BINANCE_API_SECRET", "default_secret")
    BYBIT_API_KEY: str = os.getenv("BYBIT_API_KEY", "default_key")
    BYBIT_API_SECRET: str = os.getenv("BYBIT_API_SECRET", "default_secret")
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "your_token_here")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "your_chat_id")

    # Genel Ayarlar
    LOG_LEVEL: str = "INFO"
    SISTEM_MODU: str = "PAPER" # LIVE, PAPER, BACKTEST
    
    class Config:
        env_file = ".env"
        extra = "ignore" # Ekstra değişkenler gelirse hata verme

# --- KRİTİK NOKTA BURASI ---
# Sınıfı tanımladık, şimdi onu çalıştırılabilir bir objeye dönüştürüyoruz.
# logger.py ve diğer tüm dosyalar bu 'settings' değişkenini çağırır.
settings = Settings() 
