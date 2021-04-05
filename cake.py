from web3 import Web3
import requests
import json


erc20_abi = json.loads('[{"constant": true,"inputs": [],"name": "name","outputs": [{"name": "","type": "string"}],"payable": false,"stateMutability": "view","type": "function"},{"constant": false,"inputs": [{"name": "_spender","type": "address"},{"name": "_value","type": "uint256"}],"name": "approve","outputs": [{"name": "","type": "bool"}],"payable": false,"stateMutability": "nonpayable","type": "function"},{"constant": true,"inputs": [],"name": "totalSupply","outputs": [{"name": "","type": "uint256"}],"payable": false,"stateMutability": "view","type": "function"},{"constant": false,"inputs": [{"name": "_from","type": "address"},{"name": "_to","type": "address"},{"name": "_value","type": "uint256"}],"name": "transferFrom","outputs": [{"name": "","type": "bool"}],"payable": false,"stateMutability": "nonpayable","type": "function"},{"constant": true,"inputs": [],"name": "decimals","outputs": [{"name": "","type": "uint8"}],"payable": false,"stateMutability": "view","type": "function"},{"constant": true,"inputs": [{"name": "_owner","type": "address"}],"name": "balanceOf","outputs": [{"name": "balance","type": "uint256"}],"payable": false,"stateMutability": "view","type": "function"},{"constant": true,"inputs": [],"name": "symbol","outputs": [{"name": "","type": "string"}],"payable": false,"stateMutability": "view","type": "function"},{"constant": false,"inputs": [{"name": "_to","type": "address"},{"name": "_value","type": "uint256"}],"name": "transfer","outputs": [{"name": "","type": "bool"}],"payable": false,"stateMutability": "nonpayable","type": "function"},{"constant": true,"inputs": [{"name": "_owner","type": "address"},{"name": "_spender","type": "address"}],"name": "allowance","outputs": [{"name": "","type": "uint256"}],"payable": false,"stateMutability": "view","type": "function"},{"payable": true,"stateMutability": "payable","type": "fallback"},{"anonymous": false,"inputs": [{"indexed": true,"name": "owner","type": "address"},{"indexed": true,"name": "spender","type": "address"},{"indexed": false,"name": "value","type": "uint256"}],"name": "Approval","type": "event"},{"anonymous": false,"inputs": [{"indexed": true,"name": "from","type": "address"},{"indexed": true,"name": "to","type": "address"},{"indexed": false,"name": "value","type": "uint256"}],"name": "Transfer","type": "event"}]')
web3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))


# dai_usdt - dai_busd - usdt_usdc - usdc-busd - usdt_busd - ust_busd
pairs = [
"0xb3c4217AB2b265bF8c69718D280E3708b5E50577", "0x3aB77e40340AB084c3e23Be8e5A6f7afed9D41DC", 
"0x85F8628BFFF75D08F1Aa415E5C7e85d96bfD7f57", "0x680Dd100E4b394Bda26A59dD5c119A391e747d18",
"0xc15fa3E22c912A276550F3E5FE3b0Deb87B55aCd", "0xD1F12370b2ba1C79838337648F820a87eDF5e1e6"
]

def getErc20Balance(addressContract, addressToken):
    try:
        contract = web3.eth.contract((Web3.toChecksumAddress(addressToken)), abi=erc20_abi)
        balance = contract.functions.balanceOf(addressContract).call()
        return (balance/(10**18))
    except:
        return 0

def getPairs() :
    try:
        r = requests.get('https://api.pancakeswap.finance/api/v1/stat')
        if (r.status_code != 200):
            return []
        my_json = r.content.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        allPairs = data["trade_pairs"]
        stablesPairs = []
        for x in allPairs :
            if x['swap_pair_contract'] in pairs :
                stablesPairs.append(x)
        return stablesPairs
    except:
        return []


def getStats() :
    info = getPairs()
    if(info == []):
        return []
    f = []
    for x in info:
        totalQuoteLiquidity= getErc20Balance(x['swap_pair_contract'], x['quote_address'])
        if totalQuoteLiquidity == 0 :
            return 0
        d = {}
        d['base_symbol'] = x['base_symbol']
        d['quote_symbol'] = x['quote_symbol']
        d['last_price'] = x['last_price']
        d['daily_fees_per_1k'] = (500 / totalQuoteLiquidity)*(x['quote_volume_24_h'] * 0.002)
        d['daily_roi'] = (d['daily_fees_per_1k']/1000)*100
        d['annual_roi'] = d['daily_roi']*365
        f.append(d)
    return f