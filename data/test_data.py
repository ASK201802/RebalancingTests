"""Test data payloads for portfolio rebalancing tests.

Defines rebalance request payloads for various test scenarios including
normal rebalancing, empty payloads, invalid securities, single allocations,
and no-change scenarios.
"""

from models.rebalance import RebalanceRequest, TradeRequest

ACCOUNT_ID = "PORT_REBAL_100"

# Standard rebalance payload: BUY IBM (10% -> 20%), SELL ORCL (30% -> 20%)
REBALANCE_PAYLOAD = RebalanceRequest(
    account_id=ACCOUNT_ID,
    total_allocated_assets=100000,
    trades=[
        TradeRequest(
            security_name="IBM",
            current_percentage=10.00,
            target_percentage=20.00,
            action="BUY",
            target_valriance=10.00,
            unit_price=150.00,
        ),
        TradeRequest(
            security_name="ORCL",
            current_percentage=30.00,
            target_percentage=20.00,
            action="SELL",
            target_valriance=10.00,
            unit_price=220.00,
        ),
    ],
)

# Empty payload with no trades - used for bad request validation
EMPTY_PAYLOAD = RebalanceRequest(
    account_id=ACCOUNT_ID,
    total_allocated_assets=0,
    trades=[],
)

# Payload with an invalid security name - used for bad request validation
WRONG_SECURITY_PAYLOAD = RebalanceRequest(
    account_id=ACCOUNT_ID,
    total_allocated_assets=100000,
    trades=[
        TradeRequest(
            security_name="Invalid Security",
            current_percentage=10.00,
            target_percentage=20.00,
            action="BUY",
            target_valriance=10.00,
            unit_price=150.00,
        ),
        TradeRequest(
            security_name="ORCL",
            current_percentage=30.00,
            target_percentage=20.00,
            action="SELL",
            target_valriance=10.00,
            unit_price=220.00,
        ),
    ],
)

# Single security payload targeting 100% allocation for IBM - boundary value test
SINGLE_IBM_PAYLOAD = RebalanceRequest(
    account_id=ACCOUNT_ID,
    total_allocated_assets=100000,
    trades=[
        TradeRequest(
            security_name="IBM",
            current_percentage=10.00,
            target_percentage=100.00,
            action="BUY",
            target_valriance=90.00,
            unit_price=150.00,
        ),
    ],
)

# Single security payload with no change (current == target) - used to verify idempotency
SINGLE_SECURITY_NO_CHANGE_PAYLOAD = RebalanceRequest(
    account_id=ACCOUNT_ID,
    total_allocated_assets=100000,
    trades=[
        TradeRequest(
            security_name="IBM",
            current_percentage=20.00,
            target_percentage=20.00,
            action="BUY",
            target_valriance=0.00,
            unit_price=150.00,
        ),
    ],
)

# Known security ticker symbols in the portfolio
security_names = ["IBM", "MSFT", "ORCL", "AAPL", "HD"]
