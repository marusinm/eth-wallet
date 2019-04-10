from web3 import Web3, HTTPProvider

# use from web3.auto.infura import w3 instedead (api key is as exported variable)
w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/57caa86e6f454063b13d717be8cc3408"))
print(w3.isConnected())
print(w3.eth.blockNumber)
print(w3.eth.getBlock('latest'))
