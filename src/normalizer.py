def normalize(tick):
    return {
        "source": tick.get("source"),
        "pair": tick.get("pair"),
        "price": float(tick.get("price", 0)),
        "volume": float(tick.get("volume", 0)),
        "liquidity": float(tick.get("liquidity", tick.get("liquidity_depth", 0))),
        "raw": tick.get("raw"),
        "timestamp": tick.get("timestamp")
    }
