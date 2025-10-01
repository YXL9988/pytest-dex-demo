import pytest

@pytest.mark.smoke
@pytest.mark.happy
def test_add_liquidity_happy_and_pool_info(dex, usdc_weth_pool):
    res = dex.add_liquidity(pool_id=usdc_weth_pool, amountA=1_000_000, amountB=3.2e14, price_min=3000, price_max=5000)
    assert res["status"] == "ADDED"

    p = dex.get_pool(usdc_weth_pool)
    for k in ("tokenA", "tokenB", "liquidity"):
        assert k in p

@pytest.mark.happy
def test_add_liquidity_check_accumulate(dex, usdc_weth_pool):
    res1 = dex.add_liquidity(pool_id=usdc_weth_pool, amountA=1000, amountB=2000, price_min=3000, price_max=5000)
    assert res1["status"] == "ADDED"
    res2 = dex.add_liquidity(pool_id=usdc_weth_pool,amountA=500, amountB=2000, price_min=3000, price_max=5000)
    assert res2["status"] == "ADDED"

    assert dex.get_pool(usdc_weth_pool)["liquidity"] >= 1500

@pytest.mark.negative
def test_liquidity_rejects_bad_price_range(dex,usdc_weth_pool):
    res = dex.add_liquidity(pool_id=usdc_weth_pool, amountA=100, amountB=100, price_min=5000, price_max=3000)
    assert res["status"] == "REJECTED"
    assert res["reason"] == "BAD_PRICE_RANGE"

@pytest.mark.negative
def test_liquidity_rejects_bad_amounts(dex,usdc_weth_pool):
    res = dex.add_liquidity(pool_id=usdc_weth_pool, amountA=0, amountB=100, price_min=1000, price_max=2000)
    assert res["status"] == "REJECTED"
    assert res["reason"] == "BAD_AMOUNTS"

@pytest.mark.negative
def test_nonexistent_pool(dex):
    res = dex.add_liquidity(pool_id="FAKE-POOL", amountA=1000, amountB=1000, price_min=3000, price_max=5000)
    assert res["status"] == "REJECTED" and res["reason"] == "POOL_NOT_FOUND"

@pytest.mark.edge
def test_liquidity_overflow(dex, usdc_weth_pool):
    res = dex.add_liquidity(pool_id=usdc_weth_pool,amountA=10**30, amountB=10**30, price_min=3000, price_max=5000)
    assert res["status"] == "REJECTED" and res["reason"] == "OVERFLOWS"


@pytest.mark.negative
def test_liquidity_bad_ratio(dex, usdc_weth_pool):
    res = dex.add_liquidity(pool_id=usdc_weth_pool,amountA=10**18, amountB=1, price_min=3000, price_max=5000)
    assert res["status"] == "REJECTED" and res["reason"] == "BAD_RATIO"

@pytest.mark.edge
def test_fee_accumulates_in_pool(dex, usdc_weth_pool):
    pool_before = dex.get_pool(usdc_weth_pool)["liquidity"]

    q = dex.get_quote(amount_in=1_000_000, pool_id=usdc_weth_pool,slippage_bps=50)

    res = dex.submit_swap(
        pool_id=usdc_weth_pool,
        actual_out=q["expected_out_after_fee"],
        min_out=q["minOut"],
        quoted_fee=q["fee"]
    )
    assert res["status"] == "SUCCESS"
    pool_after = dex.get_pool(usdc_weth_pool)["liquidity"]
    assert pool_after > pool_before
