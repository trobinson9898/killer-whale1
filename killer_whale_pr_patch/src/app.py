import asyncio, logging
from asyncio import Queue
from src.connector_dexscreener import poll_pairs
from src.connector_geckoterminal import poll_geckoterminal
from src.normalizer import normalize
from src.features import FeatureStore
from src.mode_controller import ModeController
from src.signal_engine import generate_signal
from src.execution import execute_signal
from src.risk_engine import sizing
from src.config import load_config

async def main():
    logging.basicConfig(level=logging.INFO)
    cfg = load_config()
    q = Queue()
    fs = FeatureStore(window=200)
    mc = ModeController(cfg)

    tasks = []
    if cfg['feeds']['dexscreener']['enabled']:
        tasks.append(asyncio.create_task(poll_pairs(q, poll_interval=cfg['feeds']['dexscreener']['poll_interval_seconds'])))
    if cfg['feeds']['geckoterminal']['enabled']:
        tasks.append(asyncio.create_task(poll_geckoterminal(q, poll_interval=cfg['feeds']['geckoterminal']['poll_interval_seconds'])))

    equity = 10000.0
    try:
        while True:
            tick = await q.get()
            norm = normalize(tick)
            fs.add_tick(norm)

            pair = norm['pair']
            V = fs.atr_approx(pair)
            L = fs.liquidity_median(pair)
            T = 0.65
            W = 0.0

            mode = mc.decide_mode(V, L, T, W)
            feat = {"dexscreener": {"V":V,"L":L}}
            last = fs.vwaps(pair)
            if last and last.get('last_price',0) > last.get('vwap',0) * 1.002:
                sig = generate_signal(pair, "long", last['last_price'], feat, mode)
                plan_notional = sizing(equity, cfg['risk']['max_risk_per_trade_pct'], sig['entry_price'], sig['stop_loss'])
                await execute_signal(sig, cfg)
            q.task_done()
    except asyncio.CancelledError:
        for t in tasks: t.cancel()

if __name__ == "__main__":
    asyncio.run(main())
