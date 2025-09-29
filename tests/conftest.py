import pytest
from src.dex import Dex

@pytest.fixture
def dex():
    return Dex()

@pytest.fixture
def usdc_weth_pool(dex):
    pool_id = "pool-usdc-weth"
    dex.add_pool(pool_id, "USDC", "WETH")
    return pool_id

@pytest.fixture(scope="session")
def default_rate():
    return 0.00032
