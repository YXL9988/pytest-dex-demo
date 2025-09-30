import pytest

@pytest.mark.smoke
@pytest.mark.happy
def test_add_liquidity_happy_and_pool_info(dex, usdc_weth_pool):
    res = dex.add_liquidity(pool_id=usdc_weth_pool, amountA=1_000_000, amountB=3.2e14, price_min=3000, price_max=5000)
    assert res["status"] == "ADDED"

    p = dex.get_pool(usdc_weth_pool)
    for k in ("tokenA", "tokenB", "liquidity"):
        assert k in p

@pytest.mark.negative
def test_liquidity_negative_cases(dex, usdc_weth_pool):
    bad1 = dex.add_liquidity(pool_id=usdc_weth_pool, amountA=100, amountB=100, price_min=2000, price_max=1000)
    assert bad1["status"] == "REJECTED" and bad1["reason"] == "BAD_PRICE_RANGE"

    bad2 = dex.add_liquidity(pool_id=usdc_weth_pool, amountA=0, amountB=100, price_min=1000, price_max=2000)
    assert bad2["status"] == "REJECTED" and bad2["reason"] == "BAD_AMOUNTS"
