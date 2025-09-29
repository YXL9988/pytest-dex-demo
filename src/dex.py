class Dex:
    def __init__(self):
        self.pools = {}

    def add_pool(self, pool_id, tokenA, tokenB):
        self.pools[pool_id] = {"tokenA": tokenA, "tokenB": tokenB, "liquidity": 0}
        return pool_id

    def get_quote(self, amount_in, rate, slippage_bps):
        if amount_in <= 0:
            raise Exception("Invalid amount")
        if slippage_bps <= 0:
            raise Exception("Invalid slippage")

        expected_out = amount_in * rate
        min_out = expected_out * (1 - slippage_bps / 10000)
        return {"expectedOut": expected_out, "minOut": min_out}

    def submit_swap(self, actual_out, min_out):
        if actual_out < min_out:
            return {"status": "REVERTED", "reason": "SLIPPAGE_EXCEEDED"}
        return {"status": "SUCCESS"}

    def add_liquidity(self, pool_id, amountA, amountB, price_min, price_max):
        if amountA <= 0 or amountB <= 0:
            return {"status": "REJECTED", "reason": "BAD_AMOUNTS"}
        if price_min >= price_max:
            return {"status": "REJECTED", "reason": "BAD_PRICE_RANGE"}
        self.pools[pool_id]["liquidity"] += amountA + amountB
        return {"status": "ADDED"}

    def get_pool(self, pool_id):
        return self.pools.get(pool_id, {})
