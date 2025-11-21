def sizing(equity, risk_pct, entry_price, stop_loss_price):
    if stop_loss_price is None or entry_price == 0: return 0
    stop_loss_pct = abs(entry_price - stop_loss_price) / entry_price
    if stop_loss_pct <= 0: return 0
    risk_amount = equity * (risk_pct/100.0)
    position_notional = risk_amount / stop_loss_pct
    return position_notional
