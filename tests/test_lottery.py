# 0.01231527093
# 12,315,270,930,000,000
# 24,627,811,894,445,000
# 12,291,686,640,657,457 > 122,000,000,000,000,000
from brownie import Lottery, accounts, config, network
from web3 import Web3


def test_get_enterance_fee():
    account = accounts[0]
    print(network.show_active())
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )
    print(lottery)
    print(f"The price is {lottery.getEnteranceFee()}")
    assert lottery.getEnteranceFee() > Web3.toWei(0.01201527093, "ether")
    assert lottery.getEnteranceFee() < Web3.toWei(0.13, "ether")
