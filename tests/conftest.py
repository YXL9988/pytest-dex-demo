import copy, json, os, pytest
from src.dex import Dex

@pytest.fixture
def dex():
    pool_file = os.getenv("DEX_POOL_FILE","data/pools_sample.json")
    d = Dex(pool_file=pool_file)
    d.pools = copy.deepcopy(d.pools)
    return d

@pytest.fixture
def usdc_weth_pool(dex):
    pool_id = "USDC-WETH"
    if pool_id not in dex.pools:
        dex.add_pool(pool_id, "USDC", "WETH")
    # dex.add_liquidity(pool_id, amountA=1_000_000, amountB=1_000_000, price_min=3000, price_max=5000)
    assert "liquidity" in dex.pools[pool_id]
    return pool_id

@pytest.fixture
def usdc_weth_pool_empty(dex):
    pool_id = "USDC-WETH"
    if pool_id not in dex.pools:
        dex.add_pool(pool_id, tokenA="USDC", tokenB="WETH")
    dex.pools[pool_id]["liquidity"] = 0
    return pool_id

@pytest.fixture
def usdc_weth_pool_high_fee(dex, usdc_weth_pool):
    dex.pools[usdc_weth_pool]["fee_bps"] = 100  # 1%
    return usdc_weth_pool

@pytest.fixture(scope="session") #for test_extreme_low_rate
def test_rate():
    return 0.000001
