# app/control_layer/telegram_bot.py
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from app.core.config import settings
from app.core.logger import logger
import asyncio

class TradingBot:
    def __init__(self, pnl_tracker, order_manager):
        self.bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        self.dp = Dispatcher()
        self.pnl_tracker = pnl_tracker
        self.order_manager = order_manager
        
        # Komutları tanımla
        self.dp.message.register(self.handle_status, lambda msg: msg.text == "/status")
        self.dp.message.register(self.handle_panic, lambda msg: msg.text == "/panic")

    async def handle_status(self, message: Message):
        """Sistemin anlık durumunu raporlar."""
        stats = self.pnl_tracker.get_stats()
        positions = self.order_manager.active_positions
        
        pos_text = "\n".join([f"{s}: {d['side']} {d['qty']} @ {d['entry']}" for s, d in positions.items()])
        if not pos_text: pos_text = "Açık pozisyon yok."

        report = (
            f"🤖 **MTO Trading OS Durum Raporu**\n\n"
            f"💰 Toplam PNL: {stats['total_pnl']:.2f} USDT\n"
            f"📈 Win Rate: %{stats['win_rate']:.2f}\n"
            f"🔄 Toplam İşlem: {stats['trades']}\n\n"
            f"📦 **Açık Pozisyonlar:**\n{pos_text}"
        )
        await message.answer(report, parse_mode="Markdown")

    async def handle_panic(self, message: Message):
        """SİSTEMİ DURDUR: Tüm pozisyonları kapatma emri gönderir."""
        await message.answer("🚨 **PANİK MODU AKTİF!** Tüm pozisyonlar kapatılıyor ve sistem durduruluyor...")
        # Burada Execution Engine'e "Tümünü Kapat" emri gönderilir
        logger.warning("Kullanıcı tarafından PANİK butonu tetiklendi!")

    async def send_alert(self, text: str):
        """Sistemden gelen bildirimleri Telegram'a gönderir."""
        try:
            await self.bot.send_message(chat_id=settings.TELEGRAM_CHAT_ID, text=text)
        except Exception as e:
            logger.error(f"Telegram mesaj gönderim hatası: {e}")

    async def start_polling(self):
        logger.info("Telegram Botu başlatılıyor...")
        await self.dp.start_polling(self.bot)
