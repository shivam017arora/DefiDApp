from scripts import deploy
from brownie import network, exceptions
from scripts import helper
import pytest

def test_set_price_feed_contract():
    #Arrange
    if(network.show_active() not in helper.LCBE):
        pytest.skip()
    account = helper.get_account()
    non_owner_account = helper.get_account(index=2)
    token_farm, dapp_token = deploy.deploy_token_and_farm()

    #Act
    token_farm.setPriceFeedContract(
                                dapp_token.address, 
                                helper.get_contract('eth_usd_price_feed'),
                                {'from': account})
    
    #Assert
    assert token_farm.tokenPriceFeedMapping(dapp_token.address) == helper.get_contract('eth_usd_price_feed')
    with pytest.raises(exceptions.VirtualMachineError):
        #Assert
        token_farm.setPriceFeedContract(
                        dapp_token.address, 
                        helper.get_contract('eth_usd_price_feed'), 
                        {'from': non_owner_account})

def test_stake_tokens(amount_staked):
    #Arrange
    if(network.show_active() not in helper.LCBE):
        pytest.skip()
    account = helper.get_account()
    token_farm, dapp_token = deploy.deploy_token_and_farm()

    #Act
    #1. Approve on ERC20 token
    dapp_token.approve(token_farm.address, amount_staked, {'from': account})
    #2. Stake tokens
    token_farm.stakeTokens(amount_staked, dapp_token.address)

    #Assert
    assert token_farm.stakingBalance(dapp_token.address, account.address) == amount_staked
    assert token_farm.uniqueTokensStaked(account.address) == 1
    assert token_farm.stakers(0) == account.address

    return token_farm, dapp_token


def test_issue_tokens(amount_staked):
    #Arrange
    if(network.show_active() not in helper.LCBE):
        pytest.skip()
    account = helper.get_account()
    
    token_farm, dapp_token = test_stake_tokens(amount_staked)
    starting_balance = dapp_token.balanceOf(account.address)

    #Act
    token_farm.issueTokens({'from': account})

    #Assert
    # We are staking 1 DAPP token == 1 ETH
    # so.. we should get 2000 DAPP in reward 
    # since price of ETH is $2000 USD
    assert dapp_token.balanceOf(account.address) == starting_balance + 2000000000000000000000
    
