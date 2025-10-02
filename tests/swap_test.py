import pytest

@pytest.mark.smoke
@pytest.mark.happy
def test_swap_happy_path(dex,usdc_weth_pool):
    q = dex.get_quote(pool_id=usdc_weth_pool, amount_in=1_000_000, slippage_bps=50)
    assert q["expected_out_after_fee"] > q["minOut"]
    res = dex.submit_swap(pool_id=usdc_weth_pool,actual_out=q["minOut"], min_out=q["minOut"])
    assert res["status"] == "SUCCESS"

@pytest.mark.negative
def test_swap_reverted_when_slippage_exceeded(dex,usdc_weth_pool):
    q = dex.get_quote(pool_id=usdc_weth_pool,amount_in=1_000_000, slippage_bps=50)
    res = dex.submit_swap(pool_id=usdc_weth_pool,actual_out=q["minOut"] - 1, min_out=q["minOut"])
    assert res["status"] == "REVERTED"
    assert res["reason"] == "SLIPPAGE_EXCEEDED"

@pytest.mark.negative
@pytest.mark.parametrize("amount, slippage", [(0, 50), (1000, -1)],ids=["amount_zero","slippage_negative"])
def test_quote_invalid_inputs(dex, amount, slippage):
    with pytest.raises(Exception):
        dex.get_quote(amount_in=amount, slippage_bps=slippage)

@pytest.mark.negative
def test_quote_with_negative_amount(dex):
    with pytest.raises(Exception):
        dex.get_quote(amount_in=-100, pool_id="USDC-WETH", slippage_bps=50)

@pytest.mark.negative
def test_quote_with_nonexistent_pool(dex):
    res = dex.get_quote(amount_in=1000,pool_id="FAKE-POOL", slippage_bps=50)
    assert res["status"] == "REVERTED"
    assert res["reason"] == "POOL_NOT_FOUND"

@pytest.mark.negative
def test_swap_fails_when_actual_out_too_low(dex):
    q = dex.get_quote(amount_in=1000, pool_id="USDC-WETH", slippage_bps=50)
    res = dex.submit_swap(pool_id="USDC-WETH",actual_out=q["minOut"] - 100, min_out=q["minOut"])
    assert res["status"] == "REVERTED"
    assert res["reason"] == "SLIPPAGE_EXCEEDED"

@pytest.mark.negative
def test_quote_with_new_pool_no_liquidity(dex):
    pool_id = "EMPTY-POOL"
    dex.create_pool(pool_id,"USDC","WETH",initial_liquidity=0)
    res = dex.get_quote(amount_in=1000,pool_id=pool_id,slippage_bps=50)
    assert res["status"] == "REVERTED"
    assert res["reason"] == "NO_LIQUIDITY"

@pytest.mark.negative
def test_swap_reverted_when_existing_pool_no_liquidity(dex):
    dex.pools["USDC-WETH"]["liquidity"] = 0
    q = dex.get_quote(amount_in=1000, pool_id="USDC-WETH")
    assert q["status"] == "REVERTED"
    assert q["reason"] == "NO_LIQUIDITY"

@pytest.mark.edge
def test_quote_with_max_slippage(dex):
    q = dex.get_quote(amount_in=1_000_000, slippage_bps=10000)
    assert q["minOut"] == 0
    assert q["expected_out_after_fee"] > 0

@pytest.mark.edge
def test_quote_with_large_trade_slippage_capped(dex):
    q = dex.get_quote(amount_in=10 ** 12, slippage_bps=50)
    assert "expected_out_after_fee" in q and "minOut" in q

@pytest.mark.edge
def test_quote_fails_on_empty_pool(dex,usdc_weth_pool_empty):
    res = dex.get_quote(amount_in=1000,pool_id=usdc_weth_pool_empty,slippage_bps=50)
    assert res["status"] == "REVERTED"
    assert res["reason"] == "NO_LIQUIDITY"

@pytest.mark.edge
def test_high_fee_reduces_expected_out(dex, usdc_weth_pool_high_fee):
    q = dex.get_quote(amount_in=1000000, pool_id=usdc_weth_pool_high_fee, slippage_bps=50)
    assert q["expectedOut"] > q["expected_out_after_fee"]
    assert q["expected_out_after_fee"] > q["minOut"]
    assert q["minOut"] < 1000

@pytest.mark.edge
def test_extreme_low_rate(dex, test_rate):
    q = dex.get_quote(amount_in=1_000_000, rate=test_rate, slippage_bps=50)
    assert q["expected_out_after_fee"] < 100
