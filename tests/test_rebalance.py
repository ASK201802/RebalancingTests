import pytest

from models.rebalance import RebalanceResponse, AccountResponse
from services.rebalance_service import RebalanceService
from data.test_data import ACCOUNT_ID, REBALANCE_PAYLOAD, EMPTY_PAYLOAD, WRONG_SECURITY_PAYLOAD, SINGLE_IBM_PAYLOAD, SINGLE_SECURITY_NO_CHANGE_PAYLOAD, security_names
from utility.trade_comparators import compare_shares_bought_sold, compare_total_shares, compare_target_percentages, compare_deviation_percentages, compare_unchanged_allocations

@pytest.mark.asyncio
@pytest.mark.rebalancing
@pytest.mark.HIGH
@pytest.mark.TC_REBAL_001
async def test_correct_calculation_of_units_to_buy_sell(api_context):
    """
    Test to validate the correct calculation of units to buy or sell for each security in rebalancing.
    """
    service = RebalanceService(api_context)
    payload = REBALANCE_PAYLOAD
    post_response: RebalanceResponse = await service.post_rebalance(payload)
    assert isinstance(post_response, RebalanceResponse)
    assert post_response.status == "SUCCESS"
    compare_shares_bought_sold(payload.trades, post_response.trades, payload)


@pytest.mark.asyncio
@pytest.mark.rebalancing
@pytest.mark.HIGH
@pytest.mark.TC_REBAL_002
async def test_validate_target_share_percentages_post_rebalance(api_context):
    """
    Test to validate the target share percentages before rebalacing and current percentage post rebalancing 
    are same for each security in rebalancing.
    """
    service = RebalanceService(api_context)
    get_response_before_rebalance: AccountResponse = await service.get_portfolio(
        account_id=ACCOUNT_ID, is_before_rebalance=True
    )
    payload = REBALANCE_PAYLOAD
    post_response: RebalanceResponse = await service.post_rebalance(payload)
    assert isinstance(post_response, RebalanceResponse)
    compare_target_percentages(
        payload.trades, post_response.trades, get_response_before_rebalance.securities
    )


@pytest.mark.asyncio
@pytest.mark.rebalancing
@pytest.mark.HIGH
@pytest.mark.TC_REBAL_003
async def test_validate_deviation_percentage_post_rebalance(api_context):
    """
    Test to validate the deviation percentage (after rebalancing current_percentage -  before rebalancing target_percentage )
    for each security should be 0.00.
    """
    service = RebalanceService(api_context)
    get_response_before_rebalance: AccountResponse = await service.get_portfolio(
        account_id=ACCOUNT_ID, is_before_rebalance=True
    )
    payload = REBALANCE_PAYLOAD
    post_response: RebalanceResponse = await service.post_rebalance(payload)
    assert isinstance(post_response, RebalanceResponse)
    compare_deviation_percentages(
        payload.trades, post_response.trades, get_response_before_rebalance.securities
    )


@pytest.mark.asyncio
@pytest.mark.rebalancing
@pytest.mark.HIGH
@pytest.mark.TC_REBAL_004
async def test_validate_total_number_of_shares_post_rebalance(api_context):
    """
    Test to validate the total number of shares post rebalancing.
    """
    service = RebalanceService(api_context)
    payload = REBALANCE_PAYLOAD
    post_response: RebalanceResponse = await service.post_rebalance(payload)
    assert isinstance(post_response, RebalanceResponse)
    assert post_response.status == "SUCCESS"
    compare_shares_bought_sold(payload.trades, post_response.trades, payload)
    compare_total_shares(payload.trades, post_response.trades, payload)


@pytest.mark.asyncio
@pytest.mark.rebalancing
@pytest.mark.HIGH
@pytest.mark.TC_REBAL_005
async def test_validate_company_names_after_allocation(api_context):
    """
    Test to validate the securities names after rebalancing remain unchanged.
    """
    service = RebalanceService(api_context)
    payload = REBALANCE_PAYLOAD
    post_response: RebalanceResponse = await service.post_rebalance(payload)
    assert isinstance(post_response, RebalanceResponse)
    assert post_response.status == "SUCCESS"
    for trade in post_response.trades:
        assert trade.security_name in security_names


@pytest.mark.asyncio
@pytest.mark.rebalancing
@pytest.mark.HIGH
@pytest.mark.TC_REBAL_006
async def test_validate_unchanged_allocations_post_rebalance(api_context):
    """
    Test to validate the share allocations remain unchanged 
    for the securities are not rebalanced (i.e. target variance is 0), after rebalancing.
    """
    service = RebalanceService(api_context)
    payload = REBALANCE_PAYLOAD
    account_before: AccountResponse = await service.get_portfolio(
        account_id=ACCOUNT_ID, is_before_rebalance=True
    )
    await service.post_rebalance(payload)
    account_after: AccountResponse = await service.get_portfolio(
        account_id=ACCOUNT_ID
    )
    compare_unchanged_allocations(account_before, account_after, payload.trades)



@pytest.mark.asyncio
@pytest.mark.rebalancing
@pytest.mark.HIGH
@pytest.mark.TC_REBAL_007
async def test_validate_total_investment_amount_preservation(api_context):
    """
    Test to validate the total investment amount($100K) is preserved after rebalancing.
    """
    service = RebalanceService(api_context)
    payload = REBALANCE_PAYLOAD
    response = await service.post_rebalance(payload)
    assert isinstance(response, RebalanceResponse)
    assert response.status == "SUCCESS"
    assert response.total_allocated_assets == payload.total_allocated_assets    



@pytest.mark.asyncio
@pytest.mark.rebalancing
@pytest.mark.MEDIUM
@pytest.mark.TC_REBAL_008
async def test_post_rebalance_wrong_security_name_bad_request(api_context):
    """
    Test to validate that a bad request is returned 
    when the security name is incorrect in rebalance.
    """
    service = RebalanceService(api_context)
    response = await service.post_rebalance(WRONG_SECURITY_PAYLOAD, is_wrong_param_payload=True)
    assert response == 400

@pytest.mark.asyncio
@pytest.mark.rebalancing
@pytest.mark.MEDIUM
@pytest.mark.TC_REBAL_009
async def test_post_rebalance_failure_then_success(api_context):
    """
    Test to validate that a rebalance can be retried  
    and can be successful after a failure.
    """
    service = RebalanceService(api_context)
    payload = REBALANCE_PAYLOAD
    await service.post_rebalance(payload, is_failed=True)
    post_response: RebalanceResponse = await service.post_rebalance(payload)
    assert isinstance(post_response, RebalanceResponse)
    assert post_response.status == "SUCCESS"


@pytest.mark.asyncio
@pytest.mark.rebalancing
@pytest.mark.MEDIUM
@pytest.mark.TC_REBAL_010
async def test_post_rebalance_empty_payload_bad_request(api_context):
    """
    Test to validate that a bad request is returned 
    when the rebablance payload is empty.
    """
    service = RebalanceService(api_context)
    response = await service.post_rebalance(EMPTY_PAYLOAD, is_wrong_param_payload=True)
    assert response == 400


@pytest.mark.asyncio
@pytest.mark.rebalancing
@pytest.mark.HIGH
@pytest.mark.TC_REBAL_011
async def test_unauthorized_access_to_rebalance_functionality(api_context_invalid_token):
    """
    Test to validate that unauthorized access is returned 
    when the User is not authorized to perform rebalancing..
    """
    service = RebalanceService(api_context_invalid_token)
    payload = REBALANCE_PAYLOAD
    response = await service.api_context.post(
        "/api/v1/rebalance",
        data=payload.model_dump(),
    )
    assert response.status == 401, f"Expected 401, got {response.status}"


@pytest.mark.asyncio
@pytest.mark.rebalancing
@pytest.mark.MEDIUM
@pytest.mark.TC_REBAL_012
async def test_validate_float_precision_of_shares(api_context):
    """
    Test to validate that the shares bought/sold 
    and after purchase total shares 
    are validated to be .2f precise.
    """
    service = RebalanceService(api_context)
    payload = REBALANCE_PAYLOAD
    post_response: RebalanceResponse = await service.post_rebalance(payload)
    assert isinstance(post_response, RebalanceResponse)
    for trade in post_response.trades:
        assert trade.shares_bought_sold == round(trade.shares_bought_sold, 2), (
            f"{trade.security_name}: shares_bought_sold {trade.shares_bought_sold} is not .2f precise"
        )
        assert trade.after_purchase_total_shares == round(trade.after_purchase_total_shares, 2), (
            f"{trade.security_name}: after_purchase_total_shares {trade.after_purchase_total_shares} is not .2f precise"
        )


@pytest.mark.asyncio
@pytest.mark.rebalancing
@pytest.mark.MEDIUM
@pytest.mark.TC_REBAL_013
async def test_no_change_payload_matches_initial_rebalance(api_context):
    """
    Test to validate that the rebalance payload
     with same current and target percentages 
    should return the same share allocations 
    for each securities which was before rebalancing.
    """
    service = RebalanceService(api_context)
    first_response: RebalanceResponse = await service.post_rebalance(REBALANCE_PAYLOAD)
    assert isinstance(first_response, RebalanceResponse)
    assert first_response.status == "SUCCESS"
    second_response: RebalanceResponse = await service.post_rebalance(SINGLE_SECURITY_NO_CHANGE_PAYLOAD)
    assert isinstance(second_response, RebalanceResponse)
    assert second_response.status == "SUCCESS"
    assert first_response == second_response


@pytest.mark.asyncio
@pytest.mark.rebalancing
@pytest.mark.TC_REBAL_014
@pytest.mark.MEDIUM
async def test_boundary_value_for_100_percent_target_allocation(api_context):
    """
    Test to validate that the rebalance payload with 100% 
    target allocation for one security
    should return the correct share buy/sell and 
    total shares  for each of the securities.
    """
    service = RebalanceService(api_context)
    payload = SINGLE_IBM_PAYLOAD
    post_response: RebalanceResponse = await service.post_rebalance(
        payload, is_single_allocation_total=True
    )
    assert isinstance(post_response, RebalanceResponse)
    assert post_response.status == "SUCCESS"
    compare_shares_bought_sold(payload.trades, post_response.trades, payload)
    compare_total_shares(payload.trades, post_response.trades, payload)

