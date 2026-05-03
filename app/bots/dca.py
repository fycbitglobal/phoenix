class DCABot:
    def __init__(self, symbol, base_order, safety_orders, step_pct, tp_pct):
        self.symbol = symbol
        self.base_order = base_order
        self.safety_orders = safety_orders
        self.step_pct = step_pct
        self.tp_pct = tp_pct

        self.orders = []
        self.avg_price = 0
        self.total_qty = 0
        self.active = False

    def start(self, price):
        self.active = True
        self._add_order(price, self.base_order)

    def _add_order(self, price, qty):
        self.orders.append({"price": price, "qty": qty})
        self._recalculate()

    def _recalculate(self):
        total_cost = sum(o["price"] * o["qty"] for o in self.orders)
        self.total_qty = sum(o["qty"] for o in self.orders)
        self.avg_price = total_cost / self.total_qty

    def check_add_safety(self, current_price):
        if not self.active:
            return None

        last_order_price = self.orders[-1]["price"]
        drop = ((last_order_price - current_price) / last_order_price) * 100

        if len(self.orders) < self.safety_orders and drop >= self.step_pct:
            qty = self.base_order * (1.5 ** len(self.orders))
            self._add_order(current_price, qty)
            return "NEW_ORDER"

        return None

    def check_take_profit(self, current_price):
        target = self.avg_price * (1 + self.tp_pct / 100)

        if current_price >= target:
            self.active = False
            return "TAKE_PROFIT"

        return None