import asyncio, aiohttp, logging
from datetime import datetime, timezone

BASE_URL = "https://api.dexscreener.com/latest/dex/pairs"

async def fetch_pairs(session, chain_slug='base'):
    # DexScreener public API - example endpoint (may vary)
    url = f"https://api.dexscreener.com/latest/dex/pairs/{chain_slug}"
    async with session.get(url, timeout=10) as resp:
        if resp.status != 200:
            logging.warning("DexScreener non-200: %s", resp.status)
            return []
        data = await resp.json()
        return data.get('pairs', []) or []

async def poll_pairs(queue, poll_interval=5):
    import aiohttp
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                pairs = await fetch_pairs(session)
                ts = datetime.now(timezone.utc).isoformat()
                for p in pairs[:20]:  # limit for speed
                    tick = {
                        "source":"dexscreener",
                        "pair": p.get('symbol') or f"{p.get('baseToken','')}/{p.get('quoteToken','')}",
                        "price": float(p.get('priceUsd') or p.get('price', 0)),
                        "volume": float(p.get('volumeUsd') or 0),
                        "liquidity": float(p.get('liquidity', 0)),
                        "raw": p,
                        "timestamp": ts
                    }
                    await queue.put(tick)
            except Exception as e:
                logging.exception("DexScreener poll error: %s", e)
            await asyncio.sleep(poll_interval)
