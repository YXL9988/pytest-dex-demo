import pytest

@pytest.mark.smoke
@pytest.mark.happy
def test_swap_happy_path(dex, default_rate):
    q = dex.get_quote(amount_in=1_000_000, rate=default_rate, slippage_bps=50)
    assert q["expectedOut"] > q["minOut"]
    res = dex.submit_swap(actual_out=q["minOut"], min_out=q["minOut"])
    assert res["status"] == "SUCCESS"

@pytest.mark.negative
def test_swap_reverted_when_slippage_exceeded(dex, default_rate):
    q = dex.get_quote(amount_in=1_000_000, rate=default_rate, slippage_bps=50)
    res = dex.submit_swap(actual_out=q["minOut"] - 1, min_out=q["minOut"])
    assert res["status"] == "REVERTED"
    assert res["reason"] == "SLIPPAGE_EXCEEDED"

@pytest.mark.negative
@pytest.mark.parametrize("amount, slippage", [(0, 50), (1000, -1)],ids=["amount_zero","slippage_negative"])
def test_quote_invalid_inputs(dex, default_rate, amount, slippage):
    with pytest.raises(Exception):
        dex.get_quote(amount_in=amount, rate=default_rate, slippage_bps=slippage)
