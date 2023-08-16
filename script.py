import requests
import click
from typing import Dict, List, Optional

API_ENDPOINT = "https://safe-transaction-mainnet.safe.global/api/v1/safes/{safe_address}/multisig-transactions/"

def fetch_transactions(safe_address: str) -> List[Dict]:
    """
    Fetches the transactions for a given safe address.

    Args:
        safe_address (str): The Ethereum safe address.

    Returns:
        List[Dict]: A list of transaction dictionaries.
    """
    try:
        response = requests.get(API_ENDPOINT.format(safe_address=safe_address))
        
        # Handle specific response status codes
        if response.status_code == 400:
            print("Error: Invalid data provided.")
            return []
        elif response.status_code == 422:
            print("Error: Invalid Ethereum address.")
            return []

        # Handle other unsuccessful status codes
        response.raise_for_status()

        data = response.json()

        # Ensure "results" key exists in the response
        if "results" not in data:
            print("Error: Unexpected API response format.")
            return []

        return data.get("results", [])

    except requests.RequestException as e:
        print(f"Error fetching transactions: {e}")
        return []

def count_walletconnect_transactions(transactions: List[Dict]) -> int:
    """
    Counts the number of WalletConnect transactions from a list of transactions.

    Args:
        transactions (List[Dict]): A list of transaction dictionaries.

    Returns:
        int: The count of WalletConnect transactions.
    """
    return sum(1 for tx in transactions if "WalletConnect" in tx.get("origin", ""))

@click.command()
@click.option(
    "--safe_address",
    default="0xBbA4C8eB57DF16c4CfAbe4e9A3Ab697A3e0C65D8",
    help="Safe address to fetch transactions for.",
)
def main(safe_address: str):
    """
    Main function to fetch and count WalletConnect transactions for a given safe address.

    Args:
        safe_address (str): The Ethereum safe address.
    """
    transactions = fetch_transactions(safe_address)
    count = count_walletconnect_transactions(transactions)
    print(f"Number of WalletConnect transactions for safe {safe_address}: {count}")

if __name__ == "__main__":
    main()
