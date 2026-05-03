# app/control_layer/telegram_bot.py
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from app.core.config import settings
from app.core.logger import logger
import asyncio

class TradingBot:
    def __init__(self, pnl_tracker, order_manager):
        self.pnl_tracker = pnl_tracker
        self.order_manager = order_manager
        self.bot = None
        self.dp = None

        try:
            # Token'ı doğrula ve başlat
            if settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_BOT_TOKEN != "your_token_here":
                self.bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
                self.dp = Dispatcher()
                
                # Komutları tanımla
                self.dp.message.register(self.handle_status, lambda msg: msg.text == "/status")
                self.dp.message.register(self.handle_panic, lambda msg: msg.text == "/panic")
                logger.info("✅ Telegram Botu başarıyla başlatıldı.")
            else:
                logger.warning(" Geçerli bir TELEGRAM_BOT_TOKEN bulunamadı. Bot devre dışı bırakıldı.")
        except Exception as e:
            logger.error(f"❌ Telegram Botu başlatılırken hata oluştu: {e}. Bot devre dışı.")

    async def handle_status(self, message: Message):
        if not self.bot: return
        stats = self.pnl_tracker.get_stats()
        positions = self.order_manager.active_positions
        pos_text = "\n".join([f"{s}: {d['side']} {d['qty']} @ {d['entry']}" for s, d in positions.items()])
        if not pos_text: pos_text = "Açık pozisyon yok."
        report = (f"🤖 **MTO Trading OS Durum Raporu**\n\n"
                  f"💰 Toplam PNL: {stats['total_pnl']:.2f} USDT\n"
                  f"📈 Win Rate: %{stats['win_rate']:.2f}\n"
                  f"🔄 Toplam İşlem: {stats['trades']}\n\n"
                  f"📦 **Açık Pozisyonlar:**\n{pos_text}")
        await message.answer(report, parse_mode="Markdown")

    async def handle_panic(self, message: Message):
        if not self.bot: return
        await message.answer("🚨 **PANİK MODU AKTİF!**")
        logger.warning("Kullanıcı tarafından PANİK butonu tetiklendi!")

    async def send_alert(self, text: str):
        """Sistemden gelen bildirimleri Telegram'a gönderir."""
        if not self.bot:
            return # Bot yoksa sessizce çık
        try:
            await self.bot.send_message(chat_id=settings.TELEGRAM_CHAT_ID, text=text)
        except Exception as e:
            logger.error(f"Telegram mesaj gönderim hatası: {e}")

    async def start_polling(self):
        if not self.bot or not self.dp:
            return # Bot yoksa polling başlatma
        try:
            logger.info("Telegram Botu dinlemeye başladı...")
            await self.dp.start_polling(self.bot)
        except Exception as e:
            logger.error(f"Telegram polling hatası: {e}")
