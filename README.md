# Safe Home Exploration

## 1. Create a Safe

### Question:
Create a Safe on an Ethereum Testnet (e.g. Görli) and make a transaction.

**Steps Executed**:

1. **Safe Creation**:  
   A Safe was successfully created on the Görli Testnet.  
   [View the Safe creation transaction on Etherscan](https://goerli.etherscan.io/tx/0x292543e8d908183b0fefbe99caf4ea9deec191ae00ed42f485f4401d60704da8)

2. **Funding the Safe**:  
   The Safe was funded with 90 COW Tokens.  
   [View the funding transaction on Etherscan](https://goerli.etherscan.io/tx/0xa774cd6d94c3e2ff869c3cdddd4a87ea5eebcd383c8a133ae2929b333c90087d)

3. **Diversifying the Portfolio**:  
   To diversify the assets, 45 COW Tokens from the Safe were invested to acquire GNO tokens.  
   [View the diversification transaction on Etherscan](https://goerli.etherscan.io/tx/0x469f001a99c1741e8e73148cc0cb0866cf15a679b3e9f496044b7cf9f4f60a71)

---

## 2. On-chain analytics

### Question:
Please write a simple query on Dune that would fetch the list of Safes on Ethereum mainnet that have been created but never made any transaction after creation.

### SQL Methods for Identifying Dormant Safes:

1. **NOT IN**:
   ```sql
   SELECT address 
   FROM safes s 
   WHERE s.address NOT IN (SELECT t.address FROM transactions t)
   ```
   This method fetches addresses that haven't made transactions. It can be inefficient for large datasets as it compares each address against all addresses in the subquery.

2. **NOT EXISTS**:
   ```sql
   SELECT address 
   FROM safes s 
   WHERE NOT EXISTS (SELECT 1 FROM transactions t WHERE t.address = s.address)
   ```
   This method checks the existence of a transaction for each Safe. It's efficient because the database can stop searching once a match is found.

3. **LEFT JOIN**:
   ```sql
   SELECT s.address 
   FROM safes s 
   LEFT JOIN transactions t ON s.address = t.address 
   WHERE t.address IS NULL
   ```
   This method identifies Safes without transactions using a join. It's performant, especially with proper indexing, as join operations are optimized in most databases.

**Performance Analysis**:
Using the `EXPLAIN ANALYZE` feature inside of Dune, the following observations were made:
- **NOT EXISTS** was the most performant, likely due to early exit on match detection.
- **LEFT JOIN** was a close second, slightly slower than `NOT EXISTS`.
- **NOT IN** was the least performant, especially with large datasets.

**Dune Query Link**:  
[https://dune.com/queries/2876814](https://dune.com/queries/2876814)

**Conclusion**: 
For this specific task, and based on the insights from `EXPLAIN ANALYZE` in Dune, the `NOT EXISTS` method proved to be the most efficient.

---

## 3. APIs

### Question:
Please write a script that uses the endpoint `https://safe-transaction-mainnet.safe.global/api/v1/safes/0xBbA4C8eB57DF16c4CfAbe4e9A3Ab697A3e0C65D8/multisig-transactions/` to count the number of “WalletConnect transactions” made with this Safe (`0xBbA4C8eB57DF16c4CfAbe4e9A3Ab697A3e0C65D8`). “WalletConnect transactions” are those that contain the word “WalletConnect” in the “origin” field of the response.

Solution:
The solution to this problem can be found in the `script.py` file. Here's a snippet of the solution:

```python
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

```

For the complete solution and to run the script, please refer to the `script.py` file. Additionally, a `requirements.txt` file has been included to ensure all dependencies are easily installable.

## Potential questions during the interview

- What metrics and KPIs would you track for the Safe?
- How and where would you make them available for the team?
- How comfortable would you be using Dune (SQL) for onchain analysis?
- How comfortable would you be using GA & GTM for product analytics?
- How comfortable would you be using one of the APIs?
○ How would you query data from APIs?
- How would you connect analytics data across different systems (UI tracking,
on-chain analytics, APIs)?
- How do you imagine being involved in the product development process and with
which roles do you anticipate to interact on a regular basis?
- How do you balance long-term projects vs ad-hoc analysis?