# Pytest DEX Demo

A simplified demo project to showcase **pytest framework** with basic DEX (Decentralized Exchange) trading flows:
- Swap (happy path & slippage exceeded)
- Liquidity pool (add / invalid cases)
- Pytest fixtures (conftest)

## Project Structure
- `src/` : Core DEX: quote/swap/pool/liquidity
- `tests/` : Test cases
- `conftest.py` : Pytest fixtures
- `pytest.ini` : Pytest config
- `requirements.txt` : Pytest config
- `README.md` : Pytest config

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