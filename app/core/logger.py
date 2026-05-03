# app/core/logger.py
import logging
import sys
from .config import settings

class SafeFormatter(logging.Formatter):
    """
    Windows konsolundaki UnicodeEncodeError hatalarını engellemek için
    tanımsız karakterleri (emojileri) temizleyen özel formatter.
    """
    def format(self, record):
        # Orijinal mesajı al
        msg = super().format(record)
        # Mesajdaki emoji ve özel karakterleri temizle (ASCII dışındakileri kaldırır)
        return msg.encode('ascii', 'ignore').decode('ascii')

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL)

    # Log formatı
    log_format = '%(asctime)s | %(levelname)s | %(module)s:%(lineno)d | %(message)s'

    # --- KONSOL ÇIKTISI (Safe Mode) ---
    console_handler = logging.StreamHandler(sys.stdout)
    # Normal formatter yerine bizim SafeFormatter'ı kullanıyoruz
    console_handler.setFormatter(SafeFormatter(log_format))
    logger.addHandler(console_handler)

    # --- DOSYA ÇIKTISI (UTF-8) ---
    # Dosyada emojiler kalsın, çünkü dosya okuyucular (VS Code, Notepad++) UTF-8 destekler.
    try:
        file_handler = logging.FileHandler("logs/system.log", encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Log dosyası oluşturulamadı: {e}")

    return logger

logger = setup_logger()
