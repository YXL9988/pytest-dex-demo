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
    dex.add_liquidity(
        pool_id,
        amountA=1_000_000,
        amountB=1_000_000,
        price_min=3000,
        price_max=5000
    )
    return pool_id

@pytest.fixture(scope="session")
def test_rate():
    return 0.000001
