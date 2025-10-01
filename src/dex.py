import json, os

class Dex:
    def __init__(self,base_rate=0.00025,fee_bps=30,pool_file=None):
        self.base_rate = base_rate
        self.fee_bps = fee_bps
        self.pools = {}

        if pool_file and os.path.exists(pool_file):
            with open(pool_file,"r") as f:
                self.pools = json.load(f)
        else:
            #fallback
            self.pools = {"USDC-WETH":{"tokenA": "USDC", "tokenB": "WETH", "liquidity": 5_000_000, "fee": fee_bps}}

    def add_pool(self, pool_id, tokenA, tokenB,initial_liquidity=0):
        self.pools[pool_id] = {
            "tokenA": tokenA,
            "tokenB": tokenB,
            "liquidity": max(0,initial_liquidity),
            "fee": self.fee_bps,
        }
        return pool_id

    def add_liquidity(self, pool_id, amountA, amountB, price_min, price_max):
        if amountA <= 0 or amountB <= 0:
            return {"status": "REJECTED", "reason": "BAD_AMOUNTS"}
        if price_min >= price_max:
            return {"status": "REJECTED", "reason": "BAD_PRICE_RANGE"}
        if pool_id not in self.pools:
            return {"status": "REJECTED", "reason": "POOL_NOT_FOUND"}
        if amountA > 1e18 or amountB > 1e18:
            return {"status": "REJECTED", "reason": "OVERFLOWS"}
        if amountA / max(amountB, 1) > 1e16:
            return {"status": "REJECTED", "reason": "BAD_RATIO"}

        self.pools[pool_id]["liquidity"] += amountA

        return {"status": "ADDED"}

    def _apply_fee(self,amount_out, fee_bps):
        fee = amount_out * (fee_bps/10_000)
        return amount_out - fee, fee

    def _effective_rate(self,amount_in,pool_id):
        if not pool_id in self.pools:
            return None, {"status": "REVERTED", "reason": "POOL_NOT_FOUND"}

        l = self.pools.get(pool_id,{}).get("liquidity",0) #fallback if no pool id no liquidity
        if l <= 0:
            return None, {"status": "REVERTED", "reason": "NO_LIQUIDITY"}
        l_impact = min(amount_in/max(l,1),0.10) # slippage cap assumption
        return self.base_rate * (1-l_impact), None # actual rate depends on liquidity and amount_in

    def get_quote(self, amount_in,pool_id="USDC-WETH", rate=None, slippage_bps=50):
        if amount_in <= 0:
            raise Exception("Invalid amount")
        if slippage_bps <= 0:
            raise Exception("Invalid slippage")
        if rate is None:
            rate, err = self._effective_rate(amount_in,pool_id)
            if err:
                return err
        pool = self.pools.get(pool_id,{})
        fee_bps = pool.get("fee_bps",self.fee_bps)

        expected_out = amount_in * rate # pre-fee
        expected_out_after_fee, fee = self._apply_fee(expected_out,fee_bps)
        min_out = expected_out_after_fee * (1 - slippage_bps / 10000)
        return {
            "expectedOut": int(expected_out),
            "fee":float(fee),
            "expected_out_after_fee": int(expected_out_after_fee),
            "minOut": int(min_out)
        }

    def submit_swap(self, pool_id,actual_out, min_out, quoted_fee=None):
        if actual_out < min_out:
            return {"status": "REVERTED", "reason": "SLIPPAGE_EXCEEDED"}
        if quoted_fee is not None and pool_id in self.pools:
            self.pools[pool_id]["liquidity"] += quoted_fee
        return {"status": "SUCCESS"}

    def get_pool(self, pool_id="USDC-WETH"):
        return self.pools.get(pool_id, {})
