"""Pytest fixtures for the portfolio rebalancing test suite.

Configures Playwright API request contexts with appropriate base URLs
and headers for both authenticated and unauthenticated test scenarios.
"""

import logging
import os

import pytest_asyncio
from dotenv import load_dotenv
from playwright.async_api import async_playwright

load_dotenv()

logger = logging.getLogger(__name__)

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Accept-Language": "en-US",
}


@pytest_asyncio.fixture
async def api_context():
    """Provide an authenticated Playwright API request context.

    Yields:
        APIRequestContext configured with BASE_URL and default headers.
    """
    async with async_playwright() as p:
        context = await p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers=HEADERS,
        )
        logger.info(f"API context created with base_url={BASE_URL}")
        yield context
        await context.dispose()
        logger.info("API context disposed")


@pytest_asyncio.fixture
async def api_context_invalid_token():
    """Provide a Playwright API request context with an invalid authentication token.

    Yields:
        APIRequestContext configured with BASE_URL and an invalid x-api-token header.
    """
    async with async_playwright() as p:
        headers = {**HEADERS, "x-api-token": "invalid"}
        context = await p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers=headers,
        )
        logger.info(f"API context (invalid token) created with base_url={BASE_URL}")
        yield context
        await context.dispose()
        logger.info("API context (invalid token) disposed")