from internal.remote_procedure_call import get_balance_wei
from internal.utilities import ADDRESS_PATH, WEI_PER_ETH

if __name__ == "__main__":
    with open(ADDRESS_PATH) as f:
        address = f.read().strip()

    balance_wei = get_balance_wei(address)
    balance_eth = balance_wei / WEI_PER_ETH

    print(f"Address: {address}")
    print(f"Wei:     {balance_wei}")
    print(f"ETH:     {balance_eth}")
