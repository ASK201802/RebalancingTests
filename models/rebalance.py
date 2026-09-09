"""Pydantic models for portfolio rebalancing API requests and responses.

Defines the data structures for trade requests, rebalance payloads,
trade responses, and account/portfolio information.
"""

from typing import Literal

from pydantic import BaseModel, Field


class TradeRequest(BaseModel):
    """Represents a single trade request within a rebalance operation."""
    security_name: str = Field(..., description="Security ticker symbol", examples=["IBM"])
    current_percentage: float = Field(..., description="Current allocation percentage", examples=[10.00])
    target_percentage: float = Field(..., description="Target allocation percentage", examples=[20.00])
    action: Literal["BUY", "SELL"] = Field(..., description="Trade action")
    target_valriance: float = Field(..., description="Number of shares percentages to buy or sell", examples=[10.00])
    unit_price: float = Field(..., description="Price per share", examples=[150.00])


class RebalanceRequest(BaseModel):
    """Represents a full rebalance request payload containing account info and trades."""

    account_id: str = Field(..., description="Account identifier")
    total_allocated_assets: float = Field(..., description="Total allocated assets value", examples=[100.00])
    trades: list[TradeRequest] = Field(..., description="List of trades to execute")


class TradeResponse(BaseModel):
    """Represents the API response for a single executed trade."""

    security_name: str = Field(..., description="Security ticker symbol", examples=["IBM"])
    current_percentage: float = Field(..., description="Current allocation percentage", examples=[20.00])
    action_taken: str = Field(..., description="Action taken on the trade", examples=["BUY", "SELL", "HOLD"])
    shares_bought_sold: float = Field(..., description="Number of shares bought or sold", examples=[0.0667])
    after_purchase_total_shares: float = Field(..., description="Total shares after transaction", examples=[0.1333])


class RebalanceResponse(BaseModel):
    """Represents the full API response for a rebalance operation."""

    status: str = Field(..., description="Response status", examples=["SUCCESS"])
    total_allocated_assets: float = Field(..., description="Total allocated assets value", examples=[100.00])
    trades: list[TradeResponse] = Field(..., description="List of executed trades")


class Security(BaseModel):
    """Represents a security holding within a portfolio account."""

    security_name: str = Field(..., description="Security ticker symbol", examples=["IBM"])
    current_allocation_percentage: float = Field(..., description="Current allocation percentage", examples=[20.00])
    total_shares: float = Field(..., description="Total shares held", examples=[0.1333])
    unit_price: float = Field(..., description="Price per share", examples=[150.00])


class AccountResponse(BaseModel):
    """Represents the API response for a portfolio account query."""

    account_id: str = Field(..., description="Account identifier")
    total_assets: float = Field(..., description="Total assets value", examples=[100.00])
    securities: list[Security] = Field(..., description="List of securities in the account")
