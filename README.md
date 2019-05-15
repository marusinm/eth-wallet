# eth-wallet 

Command line wallet for Ethereum and ERC20 tokens.

## Installation
1. Clone this repository  
2. Optionally set virtual environment  
3. Navigate to the project's root dir and run `pip3 install .`  
4. Run `eth-wallet --help` to see if wallet was installed successfully  
 
## Usage

```
eth-wallet --help
Usage: eth-wallet [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  add-token         Add new ERC20 contract.
  get-balance       Get address balance.
  get-wallet        Get wallet account from encrypted keystore.
  list-tokens       List all added tokens.
  network           Get connected network (Mainnet, Ropsten) defined in...
  new-wallet        Creates new wallet and store encrypted keystore file.
  restore-wallet    Creates new wallet and store encrypted keystore file.
  reveal-seed       Reveals private key from encrypted keystore.
  send-transaction  Sends transaction.
```

### Create wallet
Create new wallet:
```
$ eth-wallet new-wallet   
  Passphrase from keystore: 

Account address: 0xB1f761734F00d1D368Ce6f82F755bBb3005538EB
Account pub key: 0xf94e03524a1bd803ee583a1f0de7eb1eb67a90d6802eeac22b90cfdd7ff491039441472e8db543467c0450d1b7c31b5e8f81616b99226775770f9dd531afd31a
Keystore path: /Users/Joe/.eth-wallet/keystore
Remember these words to restore eth-wallet: omit speak giant bright enable increase tube worth object timber bleak bullet
```
Show wallet:
```
$ eth-wallet get-wallet   
Account address: 0xB1f761734F00d1D368Ce6f82F755bBb3005538EB
Account pub key: 0xf94e03524a1bd803ee583a1f0de7eb1eb67a90d6802eeac22b90cfdd7ff491039441472e8db543467c0450d1b7c31b5e8f81616b99226775770f9dd531afd31a
```

### Balances
Get ETH wallet balance:
```
$ eth-wallet get-balance
Balance on address 0xB1f761734F00d1D368Ce6f82F755bBb3005538EB is: 1.234ETH
```
Add new ERC20 contract:
```
$ eth-wallet add-token
  Contract address []: 0x70a68593BAfc497AC4F24Eaf13CF68E74135bA42
  Token symbol []: ZRX
  
New coin was added! ZRX 0x70a68593BAfc497AC4F24Eaf13CF68E74135bA42
```
Get balance of ERC20 token:
```
$ eth-wallet get-balance --token ZRX
Balance on address 0xB1f761734F00d1D368Ce6f82F755bBb3005538EB is: 0.0ZRX
```

### Transactions
Send ether to another wallet
```
$ eth-wallet send-transaction 
  To address: []: 0xAAD533eb7Fe7F2657960AC7703F87E10c73ae73b
  Value to send: []: 0.01
  Password from keystore: 

transaction: {'to': '0xAAD533eb7Fe7F2657960AC7703F87E10c73ae73b', 'value': 10000000000000000, 'gas': 21000, 'gasPrice': 20000000000, 'nonce': 0, 'chainId': 3}
Pending.................
Transaction mined!
Hash of the transaction: 0x193919d1ad2dc024349ccc035a15a697987bd33e1ff04e33f878e6f89f2ebbdf
Transaction cost was: 0.00042ETH
```

Send ERC20 contract tokens to another wallet
```
$ eth-wallet send-transaction --token FIT
  To address: []: 0xAAD533eb7Fe7F2657960AC7703F87E10c73ae73b
  Value to send: []: 0.9
  Password from keystore:
 
transaction: {'to': '0x19896cB57Bc5B4cb92dbC7D389DBa6290AF505Ce', 'value': 0, 'gas': 36536, 'gasPrice': 20000000000, 'nonce': 2, 'chainId': 3, 'data': '0xa9059cbb000000000000000000000000aad533eb7fe7f2657960ac7703f87e10c73ae73b0000000000000000000000000000000000000000000000000c7d713b49da0000'}
Pending......................
Transaction mined!
Hash of the transaction: 0x118556d192c2efb13ade6ccc2f18a631e14256972af9f7ec8a67067aaafc978c
Transaction cost was: 0.00073072ETH
```

### Wallet utils
Show connected network:
```
$ eth-wallet network                
You are connected to the Ropsten network!
```
List all added tokens:
```
$ eth-wallet list-tokens
ETH
ZRX
```
Restore wallet:
```
$ eth-wallet restore-wallet
  Mnemonic sentence []: omit speak giant bright enable increase tube worth object timber bleak bullet
  Passphrase:
   
Account address: 0xB1f761734F00d1D368Ce6f82F755bBb3005538EB
Account pub key: 0xf94e03524a1bd803ee583a1f0de7eb1eb67a90d6802eeac22b90cfdd7ff491039441472e8db543467c0450d1b7c31b5e8f81616b99226775770f9dd531afd31a
Keystore path: /Users/Joe/.eth-wallet/keystore
Remember these words to restore eth-wallet: omit speak giant bright enable increase tube worth object timber bleak bullet
```
> Mnemonic sentence isn't fully compatible with BIP32 and BIP39 wallets. Therefore, only this implementation can reproduce mnemonic sentence and recreate seed!

Reveal wallet master private key:
```
$ eth-wallet reveal-seed   
  Password from keystore: 
  
Account prv key: 0x843844a23e3ae7b6a695a346c981484b554ff1718299b0b42df3045f04b94f05
```

## GUI

For the testing purpose, an additionally GUI is available. 
However, it is not recommended to use since GUI doesn't provide full functionality.
Run `eth_wallet/ui/gui.py` to launch the GUI application.
#### Example
![Alt text](doc/imgs/mac-home-page.png?raw=true "Wallet's home page!")  

