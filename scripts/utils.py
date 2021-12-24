from brownie import (
    network,
    accounts,
    config,
    MockV3Aggregator,
    Contract,
    VRFCoordinatorMock,
    LinkToken,
    interface,
)
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
DECIMALS = 8
STARTING_RICE = 200000000000

contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_account(index=None, id=None):
    """This function retuns the account by given index or id, if none
        provided it just retuns the first account from the development
        chain

    Args:
        index (int)
        id (string)

    Returns:
        account_address
    """

    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
        print(type(accounts[0]))
    return accounts.add(config["wallets"]["from_key"])


def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config
    if defuned, otherwise, it will deploy a mock version of that contract, and
    retur that mock contract.

    Args:
        contract_name (string)

    Returns:
        brownie.networ.contract.ProjectContract: The most recently deployed
            version of this contract
    """

    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )

    return contract


def deploy_mocks(decimals=DECIMALS, initial_value=STARTING_RICE):
    """This function depoys a Mock contract to the development chain

    Args:
        decimals (int)
        initial_value (int)
    """
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    account = get_account()
    MockV3Aggregator.deploy(
        decimals, Web3.toWei(initial_value, "ether"), {"from": account}
    )
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Mocks deployed...")


def fund_with_link(
    contract_address, account=None, link_token=None, amount=100000000000000000
):  # 0.1 LINK
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    # Another way of getting contract from interface
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("COntract funded with Link")
    return tx
