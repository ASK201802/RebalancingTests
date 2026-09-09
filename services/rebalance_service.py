"""Service layer for interacting with the portfolio rebalancing API.

Provides methods for posting rebalance trades and retrieving portfolio data
using Playwright's async API request context.
"""

import logging
from typing import Optional

from playwright.async_api import APIRequestContext

from models.rebalance import RebalanceRequest, RebalanceResponse, AccountResponse

logger = logging.getLogger(__name__)

REBALANCE_URL = "/api/v1/rebalance"
PORTFOLIO_URL = "/api/v1/portfolio"


class RebalanceService:
    """Service class for portfolio rebalance API operations.

    Attributes:
        api_context: Playwright API request context for making HTTP calls.
    """

    def __init__(self, api_context: APIRequestContext):
        """Initialize the RebalanceService with an API request context.

        Args:
            api_context: Playwright API request context configured with base URL and headers.
        """
        self.api_context = api_context

    async def post_rebalance(
        self,
        payload: RebalanceRequest,
        is_failed: Optional[bool] = None,
        is_wrong_param_payload: Optional[bool] = None,
        is_single_allocation_total: Optional[bool] = None,
    ) -> RebalanceResponse:
        """Submit a rebalance trade request to the API.

        Args:
            payload: The rebalance request payload containing trades to execute.
            is_failed: If True, expects a 500 Internal Server Error response.
            is_wrong_param_payload: If True, expects a 400 Bad Request response.
            is_single_allocation_total: If True, passes query param for single allocation scenario.

        Returns:
            RebalanceResponse on success, None if is_failed, or HTTP status code if is_wrong_param_payload.
        """
        params = {}
        if is_failed is not None:
            params["is_failed"] = str(is_failed).lower()
        if is_wrong_param_payload is not None:
            params["is_wrong_param_payload"] = str(is_wrong_param_payload).lower()
        if is_single_allocation_total is not None:
            params["is_single_allocation_total"] = str(is_single_allocation_total).lower()
        response = await self.api_context.post(
            REBALANCE_URL,
            data=payload.model_dump(),
            params=params,
        )
        logger.info(f"POST {REBALANCE_URL} params={params} status={response.status}")
        if is_failed:
            assert response.status == 500, f"Expected 500, got {response.status}"
            logger.info("Validated expected 500 response")
            return None
        if is_wrong_param_payload:
            assert response.status == 400, f"Expected 400, got {response.status}"
            logger.info("Validated expected 400 response")
            return response.status
        assert response.ok, f"POST {REBALANCE_URL} failed: {response.status}"
        body = await response.body()
        logger.info(f"POST {REBALANCE_URL} response parsed successfully")
        return RebalanceResponse.model_validate_json(body)

    async def get_portfolio(
        self,
        account_id: str,
        is_wrong_total_share: Optional[bool] = None,
        is_before_rebalance: Optional[bool] = None,
    ) -> AccountResponse:
        """Retrieve portfolio account data from the API.

        Args:
            account_id: The account identifier to query.
            is_wrong_total_share: If True, passes query param to simulate wrong total shares.
            is_before_rebalance: If True, passes query param to get pre-rebalance state.

        Returns:
            AccountResponse containing securities and allocation data.
        """
        params = {"account_id": account_id}
        if is_wrong_total_share is not None:
            params["is_wrong_total_share"] = str(is_wrong_total_share).lower()
        if is_before_rebalance is not None:
            params["is_before_rebalance"] = str(is_before_rebalance).lower()
        response = await self.api_context.get(
            PORTFOLIO_URL,
            params=params,
        )
        logger.info(f"GET {PORTFOLIO_URL} params={params} status={response.status}")
        assert response.ok, f"GET {PORTFOLIO_URL} failed: {response.status}"
        body = await response.body()
        logger.info(f"GET {PORTFOLIO_URL} response parsed successfully")
        return AccountResponse.model_validate_json(body)
