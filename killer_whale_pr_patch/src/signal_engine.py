import uuid
from datetime import datetime, timezone

def generate_signal(pair, direction, price, features, mode, confidence=0.8):
    now = datetime.now(timezone.utc).isoformat()
    return {
        "signal_id": str(uuid.uuid4()),
        "timestamp": now,
        "pair": pair,
        "direction": direction,
        "entry_price": price,
        "entry_type": "market",
        "stop_loss": price * 0.95,
        "take_profit": price * 1.10,
        "confidence": confidence,
        "features": features,
        "mode": mode,
        "sources_confirmed": list(features.keys()),
        "expected_risk_percent": 1.0,
        "ttl_seconds": 45
    }
