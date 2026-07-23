# Wallet from Scratch
## How to use
0. Setup your Python environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   python -m pip install "coincurve>=21.0.0" "pycryptodome>=3.20.0" "requests>=2.34.2"
   ```
1. Generate a new Ethereum wallet:  
   ```bash
   python private_key/create.py
   ```
   The private key will be saved in `private_key/private_key.txt`.  
2. Derive the wallet address:  
   ```bash
   python address/address.py
   ```
   The wallet address will be saved in `address.txt`.
3. Check your wallet balance:  
   ```bash
   python balance_eth.py
   python balance_token.py --token-symbol TestUSDC
   ```
   The balance of ETH and TestUSDC should be 0.0 at this point.
4. Fund your wallet on the Sepolia testnet using a faucet
   - Sepolia ETH faucet: https://cloud.google.com/application/web3/faucet 
     Select "Etherum Sepolia (0.05 ETH)" and enter your wallet address from `address.txt`.
   - Sepolia USDC faucet: https://faucet.circle.com/
     Choose "USDC" Token, select "Ethereum Sepolia" network, and enter your wallet address from `address.txt`.
5. Check your wallet balance again:  
   ```bash
   python balance_eth.py
   python balance_token.py --token-symbol TestUSDC
   ```
   You should see some balance of ETH and TestUSDC in your wallet now.
6. Send ETH to another wallet:  
   ```bash
   python send_eth.py --to 0x000000000000000000000000000000000000dEaD --send-value-wei 1000000000000000 # Send 0.001 ETH to the burn address
   ```
   The transaction details to be signed will be printed to the console. Once typed "send" to confirm, the transaction will be sent to the Sepolia testnet. The transaction hash will be printed to the console.
7. Check the transaction status
   ```bash
   python receipt.py --transaction-hash <transaction_hash>
   ``` 
   You can also check the transaction status on Sepolia Etherscan: https://sepolia.etherscan.io/tx/<transaction_hash>
8. Send TestUSDC to another wallet:  
   ```bash
   python send_token.py --to-address 0x000000000000000000000000000000000000dEaD --send-value 10000 --token-symbol TestUSDC # Send 0.01 TestUSDC to the burn address
   ```
   The transaction details to be signed will be printed to the console. Once typed "send" to confirm, the transaction will be sent to the Sepolia testnet. The transaction hash will be printed to the console.
9. Check the transaction status
   ```bash
   python receipt.py --transaction-hash <transaction_hash>
   ``` 
   You can also check the transaction status on Sepolia Etherscan: https://sepolia.etherscan.io/tx/<transaction_hash>