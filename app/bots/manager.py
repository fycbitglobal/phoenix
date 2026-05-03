class BotManager:
    def __init__(self):
        self.bots = {}

    def create_dca_bot(self, bot_id, symbol):
        self.bots[bot_id] = {
            "bot_id": bot_id,
            "symbol": symbol,
            "type": "DCA",
            "status": "ÇALIŞIYOR"
        }

    def list_bots(self):
        return list(self.bots.values())