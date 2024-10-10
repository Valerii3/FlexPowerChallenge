
class Statistic:
    def __init__(self, current_hour):
        self.current_hour = current_hour
        self.num_trades = 0
        self.num_buy = 0
        self.num_sell = 0
        self.pnl = 0.0

    def add(self, other):
        self.num_trades += other.num_trades
        self.num_buy += other.num_buy
        self.num_sell += other.num_sell
        self.pnl += other.pnl
