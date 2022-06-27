from scripts.helper import get_account, get_contract
from brownie import DappToken, TokenFarm, network, config
from web3 import Web3
import yaml
import json
import os
import shutil
import yaml

KEPT_BALANCE = Web3.toWei(100, "ether")


def deploy_token_and_farm(front_end_update=False):
    account = get_account()
    dapp_token = DappToken.deploy({"from": account})
    token_farm = TokenFarm.deploy(
        dapp_token.address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    tx = dapp_token.transfer(
        token_farm.address, dapp_token.totalSupply() - KEPT_BALANCE, {"from": account}
    )
    tx.wait(1)
    # dapp_token, weth_token, fau_token/dai
    weth_token = get_contract("weth_token")
    fau_token = get_contract("fau_token")
    dict_of_allowed_tokens = {
        dapp_token: get_contract("dai_usd_price_feed"),
        fau_token: get_contract("dai_usd_price_feed"),
        weth_token: get_contract("eth_usd_price_feed"),
    }
    add_allowed_tokens(token_farm, dict_of_allowed_tokens, account)
    if(front_end_update):
        update_front_end()
    return token_farm, dapp_token


def add_allowed_tokens(token_farm, dict_of_allowed_tokens, account):
    for token in dict_of_allowed_tokens:
        add_tx = token_farm.addAllowedTokens(token.address, {"from": account})
        add_tx.wait(1)
        set_tx = token_farm.setPriceFeedContract(
            token.address, dict_of_allowed_tokens[token], {"from": account}
        )
        set_tx.wait(1)
    return token_farm

def update_front_end():
    #send the build folder
    copy_folders_to_frontend("./build", "./front_end/src/chain-info")
    #send the frontend brownie config file in JSON format
    with open('brownie-config.yaml', 'r') as brownie:
        config_dict = yaml.load(brownie, Loader=yaml.FullLoader)
        with open("./front_end/src/brownie-config.json", 'w') as brownie_json:
            json.dump(config_dict, brownie_json)
    print("Frontend updated!")

def copy_folders_to_frontend(source, destination):
    if(os.path.exists(destination)):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)



def main():
    deploy_token_and_farm(front_end_update=True)