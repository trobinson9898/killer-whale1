import collections, statistics

class FeatureStore:
    def __init__(self, window=200):
        self.window = window
        self.data = collections.defaultdict(lambda: collections.deque(maxlen=window))

    def add_tick(self, normalized):
        pair = normalized['pair']
        self.data[pair].append(normalized)

    def vwaps(self, pair):
        ticks = list(self.data[pair])
        if not ticks: return {}
        prices = [t['price'] for t in ticks]
        vols = [t['volume'] for t in ticks]
        vwap = sum(p*v for p,v in zip(prices, vols))/ (sum(vols) + 1e-9)
        return {"vwap": vwap, "last_price": prices[-1]}

    def liquidity_median(self, pair):
        ticks = list(self.data[pair])
        if not ticks: return 0
        return statistics.median([t.get('liquidity', t.get('liquidity_depth',0)) for t in ticks])

    def atr_approx(self, pair):
        ticks = list(self.data[pair])
        if len(ticks) < 3: return 0.0
        returns = []
        for i in range(1, len(ticks)):
            a = ticks[i-1]['price']; b = ticks[i]['price']
            returns.append(abs(b-a)/ (a+1e-9))
        return statistics.pstdev(returns)
