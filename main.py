import random
import requests
import json
import time
from loguru import logger
from datetime import datetime
from colorama import Fore, Style


def get_proxy_list():
    with open("proxy.txt", "r") as f:
        recipients = [row.strip() for row in f]
    if len(recipients) == 0:
        cprint("No proxy found in config/proxies.txt", "red")
    return recipients


def get_random_proxy():
    proxies = {}
    proxy_list = get_proxy_list()
    if len(proxy_list) > 0:
        proxy = random.choice(proxy_list)
        proxy = 'http://'+proxy
        proxies = {
            'http': proxy,
            'https': proxy,
        }

    return proxies


def main(wallet): #send_graphql_request(address, cursor):
    cursor = None
    address = wallet
    url = "https://api.starkscancdn.com/graphql"
    body = """query TransactionsTableQuery(\n  $first: Int!\n  $after: String\n  $input: TransactionsInput!\n) {\n  ...TransactionsTablePaginationFragment_transactions_2DAjA4\n}\n\nfragment TransactionsTableExpandedItemFragment_transaction on Transaction {\n  entry_point_selector_name\n  calldata_decoded\n  entry_point_selector\n  calldata\n  initiator_address\n  initiator_identifier\n  main_calls {\n    selector\n    selector_name\n    calldata_decoded\n    selector_identifier\n    calldata\n    contract_address\n    contract_identifier\n    id\n  }\n}\n\nfragment TransactionsTablePaginationFragment_transactions_2DAjA4 on Query {\n  transactions(first: $first, after: $after, input: $input) {\n    edges {\n      node {\n        id\n        ...TransactionsTableRowFragment_transaction\n        __typename\n      }\n      cursor\n    }\n    pageInfo {\n      endCursor\n      hasNextPage\n    }\n  }\n}\n\nfragment TransactionsTableRowFragment_transaction on Transaction {\n  id\n  transaction_hash\n  block_number\n  transaction_status\n  transaction_type\n  timestamp\n  initiator_address\n  initiator_identifier\n  initiator {\n    is_social_verified\n    id\n  }\n  main_calls {\n    selector_identifier\n    id\n  }\n  ...TransactionsTableExpandedItemFragment_transaction\n}\n"""
    variables = {
        "first": 30,
        "after": cursor,
        "input": {
            "initiator_address": str(address),
            "transaction_types": None,
            "sort_by": "timestamp",
            "order_by": "desc",
            "min_block_number": None,
            "max_block_number": None,
            "min_timestamp": None,
            "max_timestamp": None
        }
    }

    rand_version = random.randint(114, 118)
    macos_version = random.randint(5, 7)

    headers = {
        "Content-Type": "application/json",
        "Dnt": "1",
        "Origin": "https://starkscan.co",
        "Referer": "https://starkscan.co/",
        "Sec-Ch-Ua": f'"Chromium";v="{rand_version}", "Google Chrome";v="{rand_version}", "Not=A?Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"macOS"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_{macos_version}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{rand_version}.0.0.0 Safari/537.36"
    }

    proxies = get_random_proxy()
    response = requests.post(url, json={
        "query": body,
        "variables": variables
    }, headers=headers, proxies=proxies, timeout=60)
    if response.status_code == 200:
        my_json = response.content.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        # Извлекаем значение timestamp, selector_identifier последней транзы
        timestamp = data['data']['transactions']['edges'][0]['node']['timestamp']
        selector_identifier = data['data']['transactions']['edges'][0]['node']['main_calls'][0]['selector_identifier']
        dt_datetime = datetime.utcfromtimestamp(timestamp)
        date = dt_datetime.date()

        control_date ='2023-12-07' # контрольная датаю Если последняя дата транзакции на отзыв 2FA, установку 2FA или произошла смена приватника то выделит строчку с кошельком красным цветом

        date_object = datetime.strptime(control_date, "%Y-%m-%d")

        if date_object <= dt_datetime:
            if 'setPublicKey' in selector_identifier or 'change_owner' in selector_identifier or 'remove_signer' in selector_identifier or 'escape' in selector_identifier:

                print(f"{Fore.RED}{address} {date} 'type tx' {selector_identifier}{Style.RESET_ALL}")
            else:
                print(address, date , 'type tx', selector_identifier)
        else:
            print(address, date, 'type tx', selector_identifier)
    else:
        logger.error('Request Error, response.status_code: ', response.status_code)

def run():
    with open('wallets.txt', 'r') as f: # change path
        wallets = [row.strip() for row in f]
    num = 0
    print('Total wallets', len(wallets))
    for wallet in wallets:
       try:
            num += 1
            main(wallet)
            time.sleep(random.randint(1,4))
       except Exception as err:
            logger.error(err)

if __name__ == '__main__':

    run()
