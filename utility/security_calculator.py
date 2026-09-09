"""Utility functions for calculating share numbers during portfolio rebalancing.

Provides calculations for shares to buy/sell, current share numbers,
and total shares after rebalancing based on trade requests and portfolio data.
"""

import logging

from models.rebalance import (
    RebalanceRequest,
    TradeRequest,
)

logger = logging.getLogger(__name__)


def calculate_share_numbers_to_buy_sell(
    trade_request: TradeRequest, rebalance_request: RebalanceRequest
):
    """Calculate the number of shares to buy or sell for a given trade.

    Formula: (total_allocated_assets * target_variance / 100) / unit_price

    Args:
        trade_request: The trade request containing target variance and unit price.
        rebalance_request: The rebalance request containing total allocated assets.

    Returns:
        The number of shares to buy or sell, rounded to 2 decimal places.
    """
    target_valriance = trade_request.target_valriance

    total_alocated_assets = rebalance_request.total_allocated_assets

    unit_price = trade_request.unit_price

    # Calculate the number of shares to buy or sell

    shares_to_buy_sell = round(
        (total_alocated_assets * target_valriance / 100) / unit_price, 2
    )

    logger.info(
        f"{trade_request.security_name}: shares_to_buy_sell={shares_to_buy_sell} "
        f"(total_assets={total_alocated_assets}, variance={target_valriance}, price={unit_price})"
    )

    return shares_to_buy_sell


def calculate_current_share_numbers(
    trade_request: TradeRequest, rebalance_request: RebalanceRequest
):
    """Calculate the current number of shares held for a security.

    Formula: total_allocated_assets / (current_percentage * unit_price)

    Args:
        trade_request: The trade request containing current percentage and unit price.
        rebalance_request: The rebalance request containing total allocated assets.

    Returns:
        The current number of shares, rounded to 2 decimal places.
    """
    current_share_percentage = trade_request.current_percentage

    total_alocated_assets = rebalance_request.total_allocated_assets

    unit_price = trade_request.unit_price

    # Calculate the number of current security

    current_share_numbers = round(
        total_alocated_assets / (current_share_percentage * unit_price), 2
    )

    logger.info(
        f"{trade_request.security_name}: current_share_numbers={current_share_numbers} "
        f"(total_assets={total_alocated_assets}, current%={current_share_percentage}, price={unit_price})"
    )

    return current_share_numbers


def calculate_share_total_after_rebalancing(
    trade_request: TradeRequest, rebalance_request: RebalanceRequest
):
    """Calculate the total shares after rebalancing for a security.

    Formula: (total_allocated_assets * target_percentage / 100) / unit_price

    Args:
        trade_request: The trade request containing target percentage and unit price.
        rebalance_request: The rebalance request containing total allocated assets.

    Returns:
        The total shares at target allocation, rounded to 2 decimal places.
    """
    total_alocated_assets = rebalance_request.total_allocated_assets

    unit_price = trade_request.unit_price

    target_percentage = trade_request.target_percentage

    # Total shares at target allocation = (total_assets * target%) / price

    total = (total_alocated_assets * target_percentage / 100) / unit_price

    result = round(total, 2)

    logger.info(
        f"{trade_request.security_name}: total_shares_after_rebalancing={result} "
        f"(total_assets={total_alocated_assets}, target%={target_percentage}, price={unit_price})"
    )

    return result
