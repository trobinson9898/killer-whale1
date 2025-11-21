# Killer Whale - PR Patch
This patch adds:
- DexScreener connector (polling + normalized output)
- GeckoTerminal connector (polling + red-flag checks)
- ModeController improvements
- Execution engine stub for Base (EVM) using web3.py (dry-run default)
- Risk engine wiring
- GitHub Actions CI workflow (backtest + paper smoke test + lint + docker build)
- .env.example and instructions

IMPORTANT: All execution defaults to dry-run. Replace TEST_WALLET in .env before enabling live runs.
