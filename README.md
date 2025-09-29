[![Tests](https://github.com/YXL9988/pytest-dex-demo/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/YXL9988/pytest-dex-demo/actions/workflows/tests.yml)


# Pytest DEX Demo

A simplified demo project to showcase **pytest framework** with basic DEX (Decentralized Exchange) trading flows:
- Swap (happy path & slippage exceeded)
- Liquidity pool (add / invalid cases)
- Smart Contract (Web3 API call demo)
- Pytest fixtures (conftest)


## Project Structure
- `src/` : Core DEX: quote/swap/pool/liquidity
- `tests/` : Test cases
    - `swap_test.py` : Swap trading tests  
    - `liquidity_test.py` : Liquidity pool tests  
    - `contract_api_test.py` : Web3 contract interaction demo  
    - `conftest.py` : Pytest fixtures  
- `conftest.py` : Pytest fixtures
- `pytest.ini` : Pytest config
- `requirements.txt` : Pytest config
- `README.md` : Pytest config
- `.gitignore`

## How to Run
```bash
pip install -r requirements.txt
```

```bash
pytest -v
```

```bash
pytest tests/swap_test.py -vv
```

```bash
pytest -m happy -v
```

```bash
pytest -m negative -v
```

### Web3 contract demo
This is a demo test that shows how we could call a smart contract function.
By default, it is skipped, unless you provide:

- `WEB3_RPC`: RPC endpoint (e.g. Infura/Alchemy testnet URL)
- `DEX_CONTRACT`: Contract address
- `DEX_ABI_JSON`: Path to contract ABI JSON

```bash
pytest tests/contract_api_test.py -v
```
This demo test is intentionally skipped by default, but it shows how contract-level validation could be integrated into a CI/CD pipeline once proper testnet configurations are available.
