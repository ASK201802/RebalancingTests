# Portfolio Rebalancing API - Automated Test Suite

Automated API test suite for a portfolio rebalancing service built with Pytest, Playwright, and Pydantic. Validates trade calculations, target/deviation percentages, allocation preservation, float precision, boundary values, error handling (400/401/500), and idempotency.

## Project Structure

```
AutomatedTest/
├── conftest.py                  # Pytest fixtures (API contexts)
├── data/
│   └── test_data.py             # Test payloads for various scenarios
├── models/
│   └── rebalance.py             # Pydantic request/response models
├── services/
│   └── rebalance_service.py     # API service layer (POST/GET)
├── tests/
│   └── test_rebalance.py        # Test cases (14 tests)
├── utility/
│   ├── security_calculator.py   # Share calculation functions
│   └── trade_comparators.py     # Assertion-based comparator functions
├── pyproject.toml               # Project config and pytest markers
└── .env                         # Environment variables (BASE_URL)
```

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Setup

```bash
# Activate virtual environment (PowerShell)
.\.venv\Scripts\activate.ps1

# Install dependencies (using uv)
uv sync

# Or install dependencies (using pip)
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

## Configuration

Create a `.env` file in the project root:

```
BASE_URL=http://localhost:8000
```

## Running Tests

```bash
# Run all rebalancing tests
pytest -m rebalancing -s --html=report.html --self-contained-html

# Run only HIGH priority tests
pytest -m HIGH -s

# Run only MEDIUM priority tests
pytest -m MEDIUM -s

# Run a specific test by marker
pytest -m TC_REBAL_001 -s
```

## Test Cases

| Marker | Priority | Description |
|--------|----------|-------------|
| TC_REBAL_001 | HIGH | Validate correct calculation of units to buy/sell |
| TC_REBAL_002 | HIGH | Validate target share percentages post rebalance |
| TC_REBAL_003 | HIGH | Validate deviation percentage post rebalance |
| TC_REBAL_004 | HIGH | Validate total number of shares post rebalance |
| TC_REBAL_005 | HIGH | Validate company names after allocation |
| TC_REBAL_006 | HIGH | Validate unchanged allocations post rebalance |
| TC_REBAL_007 | HIGH | Validate total investment amount preservation |
| TC_REBAL_008 | MEDIUM | Bad request with incorrect security names |
| TC_REBAL_009 | MEDIUM | Rebalance failure then success retry |
| TC_REBAL_010 | MEDIUM | Bad request with empty payload |
| TC_REBAL_011 | HIGH | Unauthorized access (401) validation |
| TC_REBAL_012 | MEDIUM | Float precision validation (.2f) |
| TC_REBAL_013 | MEDIUM | No-change payload matches initial rebalance |
| TC_REBAL_014 | MEDIUM | Boundary value for 100% target allocation |

## Test Report

After running tests, open `report.html` in a browser to view the HTML test report.