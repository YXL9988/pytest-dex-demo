import os
import pytest
web3 = pytest.importorskip("web3", reason="web3 not installed, skipping contract API tests")
from web3 import Web3

WEB3_RPC = os.getenv("WEB3_RPC")
CONTRACT_ADDR = os.getenv("DEX_CONTRACT")
ABI_PATH = os.getenv("DEX_ABI_JSON")

reason = "Web3 demo skipped: set WEB3_RPC/DEX_CONTRACT/DEX_ABI_JSON to run"
pytestmark = pytest.mark.skipif(
    not (WEB3_RPC and CONTRACT_ADDR and ABI_PATH and os.path.exists(ABI_PATH)),
    reason=reason
)

@pytest.mark.smoke
def test_contract_quote_call_demo():
    """Demo: how to call smart contract API (skip if env not set)"""
    import json

    w3 = Web3(Web3.HTTPProvider(WEB3_RPC))
    with open(ABI_PATH, "r") as f:
        dex_abi = json.load(f)

    dex = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDR), abi=dex_abi)

    assert w3.is_connected(), "Web 3 RPC not connected"
