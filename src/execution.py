import os, logging
from web3 import Web3, HTTPProvider
from dotenv import load_dotenv

load_dotenv()
RPC = os.getenv('NODE_RPC_URL', 'https://base.rpc.example')
DRY = os.getenv('DRY_RUN', 'true').lower() == 'true'
WALLET = os.getenv('TEST_WALLET_ADDRESS', '0xDEADBEEF000000000000000000000000DEADBEEF')

w3 = Web3(HTTPProvider(RPC))

async def execute_signal(signal, config):
    # Dry run: log and return
    logging.info("Execute signal (dry_run=%s): %s", DRY, signal['signal_id'])
    if DRY:
        return {"status":"filled","note":"dry_run"}
    # Production: build tx (placeholder)
    logging.info("Building tx for %s", signal['pair'])
    # TODO: implement Uniswap v3 swap via router
    return {"status":"error","note":"not_implemented"}
