"""Comparator functions for validating portfolio rebalance trade responses.

Provides assertion-based comparators for shares bought/sold, total shares,
target percentages, deviation percentages, and unchanged allocations.
"""

import logging
from typing import List

from models.rebalance import AccountResponse, RebalanceRequest, TradeRequest, TradeResponse, Security

from utility.security_calculator import calculate_share_numbers_to_buy_sell, calculate_share_total_after_rebalancing

logger = logging.getLogger(__name__)


def compare_shares_bought_sold(
    request_list: List[TradeRequest],
    response_list: List[TradeResponse],
    rebalance_request: RebalanceRequest,
) -> bool:
    """Compare shares bought/sold in the response against calculated expected values.

    Args:
        request_list: List of trade requests with trade parameters.
        response_list: List of trade responses from the API.
        rebalance_request: The rebalance request containing total allocated assets.

    Returns:
        True if all assertions pass.

    Raises:
        AssertionError: If any response trade's shares_bought_sold does not match expected.
    """
    for response_trade in response_list:
        matching_request = next(
            (
                t
                for t in request_list
                if t.security_name == response_trade.security_name
            ),
            None,
        )
        if matching_request is None:
            continue
        expected_shares = calculate_share_numbers_to_buy_sell(
            matching_request, rebalance_request
        )
        assert response_trade.shares_bought_sold == expected_shares, (
            f"{response_trade.security_name}: expected shares_bought_sold={expected_shares}, "
            f"got {response_trade.shares_bought_sold}"
        )
        logger.info(f"{response_trade.security_name}: shares_bought_sold={response_trade.shares_bought_sold} matches expected={expected_shares}")
    logger.info("compare_shares_bought_sold passed")
    return True


def compare_total_shares(
    request_list: List[TradeRequest],
    response_list: List[TradeResponse],
    rebalance_request: RebalanceRequest,
) -> bool:
    """Compare total shares after rebalancing against calculated expected values.

    Args:
        request_list: List of trade requests with trade parameters.
        response_list: List of trade responses from the API.
        rebalance_request: The rebalance request containing total allocated assets.

    Returns:
        True if all assertions pass.

    Raises:
        AssertionError: If any response trade's after_purchase_total_shares does not match expected.
    """
    for response_trade in response_list:
        matching_request = next(
            (
                t
                for t in request_list
                if t.security_name == response_trade.security_name
            ),
            None,
        )
        if matching_request is None:
            continue
        expected_total_shares = calculate_share_total_after_rebalancing(
            matching_request, rebalance_request
        )
        assert response_trade.after_purchase_total_shares == expected_total_shares, (
            f"{response_trade.security_name}: expected after_purchase_total_shares={expected_total_shares}, "
            f"got {response_trade.after_purchase_total_shares}"
        )
        logger.info(f"{response_trade.security_name}: after_purchase_total_shares={response_trade.after_purchase_total_shares} matches expected={expected_total_shares}")
    logger.info("compare_total_shares passed")
    return True


def compare_target_percentages(
    request_list: List[TradeRequest],
    response_list: List[TradeResponse],
    securities: List[Security],
) -> bool:
    """Compare current percentages post-rebalance against target percentages.

    For traded securities (action != HOLD), verifies current_percentage equals target_percentage.
    For held securities, verifies current_percentage equals the pre-rebalance allocation.

    Args:
        request_list: List of trade requests.
        response_list: List of trade responses from the API.
        securities: List of securities from the account before rebalancing.

    Returns:
        True if all assertions pass.

    Raises:
        AssertionError: If any percentage mismatch is found.
    """
    for trade in response_list:
        if trade.action_taken != "HOLD":
            matching_request = next(
                (t for t in request_list if t.security_name == trade.security_name),
                None,
            )
            assert matching_request is not None, f"No matching request for {trade.security_name}"
            assert trade.current_percentage == matching_request.target_percentage, (
                f"{trade.security_name}: expected {matching_request.target_percentage}, "
                f"got {trade.current_percentage}"
            )
        else:
            matching_security = next(
                (s for s in securities if s.security_name == trade.security_name),
                None,
            )
            assert matching_security is not None, f"No matching security for {trade.security_name}"
            assert trade.current_percentage == matching_security.current_allocation_percentage, (
                f"{trade.security_name}: expected {matching_security.current_allocation_percentage}, "
                f"got {trade.current_percentage}"
            )
        logger.info(f"{trade.security_name}: current_percentage={trade.current_percentage} validated")
    logger.info("compare_target_percentages passed")
    return True


def compare_deviation_percentages(
    request_list: List[TradeRequest],
    response_list: List[TradeResponse],
    securities: List[Security],
) -> bool:
    """Validate that deviation between current and target percentages is zero.

    For traded securities, checks abs(current_percentage - target_percentage) == 0.00.
    For held securities, checks abs(current_percentage - pre-rebalance allocation) == 0.00.

    Args:
        request_list: List of trade requests.
        response_list: List of trade responses from the API.
        securities: List of securities from the account before rebalancing.

    Returns:
        True if all assertions pass.

    Raises:
        AssertionError: If any deviation is non-zero.
    """
    for trade in response_list:
        if trade.action_taken != "HOLD":
            matching_request = next(
                (t for t in request_list if t.security_name == trade.security_name),
                None,
            )
            assert matching_request is not None, f"No matching request for {trade.security_name}"
            assert abs(trade.current_percentage - matching_request.target_percentage) == 0.00, (
                f"{trade.security_name}: deviation {abs(trade.current_percentage - matching_request.target_percentage)} != 0.00"
            )
        else:
            matching_security = next(
                (s for s in securities if s.security_name == trade.security_name),
                None,
            )
            assert matching_security is not None, f"No matching security for {trade.security_name}"
            assert abs(trade.current_percentage - matching_security.current_allocation_percentage) == 0.00, (
                f"{trade.security_name}: deviation {abs(trade.current_percentage - matching_security.current_allocation_percentage)} != 0.00"
            )
        logger.info(f"{trade.security_name}: deviation validated")
    logger.info("compare_deviation_percentages passed")
    return True


def compare_unchanged_allocations(
    account_before: AccountResponse,
    account_after: AccountResponse,
    request_list: List[TradeRequest],
) -> bool:
    """Validate that securities not involved in trades retain their allocation percentages.

    Filters out traded securities and asserts that the remaining securities
    have unchanged current_allocation_percentage between before and after rebalancing.

    Args:
        account_before: Account response before rebalancing.
        account_after: Account response after rebalancing.
        request_list: List of trade requests (used to identify traded securities).

    Returns:
        True if all assertions pass.

    Raises:
        AssertionError: If any non-traded security's allocation changed.
    """
    traded_names = {t.security_name for t in request_list}
    for security_before in account_before.securities:
        if security_before.security_name in traded_names:
            continue
        security_after = next(
            (s for s in account_after.securities if s.security_name == security_before.security_name),
            None,
        )
        assert security_after is not None, (
            f"{security_before.security_name}: not found in account after rebalance"
        )
        assert security_after.current_allocation_percentage == security_before.current_allocation_percentage, (
            f"{security_before.security_name}: expected {security_before.current_allocation_percentage}, "
            f"got {security_after.current_allocation_percentage}"
        )
        logger.info(f"{security_before.security_name}: allocation unchanged at {security_before.current_allocation_percentage}")
    logger.info("compare_unchanged_allocations passed")
    return True
