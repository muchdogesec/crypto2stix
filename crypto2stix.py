import argparse
import requests
import json
import os
import uuid
from hashlib import md5
from datetime import datetime
import stix2
from stix2 import FileSystemStore

WALLET_NAMESPACE_UUID = uuid.UUID("00abedb4-aa42-466c-9c01-fed23315a9b7")
BUNDLE_NAMESPACE_UUID = uuid.UUID("63340903-e6fa-46e4-a5e7-25c1523ca345")
EXTENSION_DEF_IDS = {
    "wallet": "extension-definition--be78509e-6958-51b1-8b26-d17ee0eba2d7",
    "transaction": "extension-definition--151d042d-4dcf-5e44-843f-1024440318e5"
}
EXTENSION_URLS = {
    "wallet": "https://raw.githubusercontent.com/muchdogesec/stix2extensions/main/extension-definitions/scos/cryptocurrency-wallet.json",
    "transaction": "https://raw.githubusercontent.com/muchdogesec/stix2extensions/main/extension-definitions/scos/cryptocurrency-transaction.json"
}

def download_extension_definitions():
    definitions = {}
    for key, url in EXTENSION_URLS.items():
        response = requests.get(url)
        definitions[key] = response.json()
    return definitions

def get_transaction_data(tx_hash):
    url = f"https://blockchain.info/rawtx/{tx_hash}"
    response = requests.get(url)
    return response.json()

def get_wallet_data(wallet_address):
    url = f"https://blockchain.info/rawaddr/{wallet_address}"
    response = requests.get(url)
    return response.json()

def create_wallet_object(address):
    wallet_id = str(uuid.uuid5(WALLET_NAMESPACE_UUID, address))
    wallet_object = {
        "type": "cryptocurrency-wallet",
        "spec_version": "2.1",
        "id": f"cryptocurrency-wallet--{wallet_id}",
        "address": address,
        "extensions": {
            EXTENSION_DEF_IDS["wallet"]: {
                "extension_type": "new-sco"
            }
        }
    }
    return wallet_object

def create_transaction_object(tx_data):
    tx_id = str(uuid.uuid5(WALLET_NAMESPACE_UUID, tx_data["hash"]))
    execution_time = datetime.utcfromtimestamp(tx_data["time"]).isoformat() + "Z"
    transaction_object = {
        "type": "cryptocurrency-transaction",
        "spec_version": "2.1",
        "id": f"cryptocurrency-transaction--{tx_id}",
        "symbol": "BTC",
        "hash": tx_data["hash"],
        "block_id": str(tx_data["block_height"]),
        "fee": str(tx_data["fee"] / 100000000),
        "execution_time": execution_time,
        "input": [
            {
                "address_ref": f"cryptocurrency-wallet--{str(uuid.uuid5(WALLET_NAMESPACE_UUID, inp['prev_out']['addr']))}",
                "amount": inp['prev_out']['value'] / 100000000
            } for inp in tx_data["inputs"] if 'addr' in inp['prev_out']
        ],
        "output": [
            {
                "address_ref": f"cryptocurrency-wallet--{str(uuid.uuid5(WALLET_NAMESPACE_UUID, out['addr']))}",
                "amount": out['value'] / 100000000
            } for out in tx_data["out"] if 'addr' in out
        ],
        "extensions": {
            EXTENSION_DEF_IDS["transaction"]: {
                "extension_type": "new-sco"
            }
        }
    }
    return transaction_object

def clear_directory(path):
    if os.path.exists(path):
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                clear_directory(file_path)
                os.rmdir(file_path)
    else:
        os.mkdir(path)

def sort_objects(objects):
    return sorted(objects, key=lambda obj: json.dumps(obj, sort_keys=True))

def main():
    parser = argparse.ArgumentParser(description="Convert crypto transactions or wallets into STIX objects")
    parser.add_argument("--transaction", type=str, help="Transaction hash")
    parser.add_argument("--wallet", type=str, help="Wallet hash")
    parser.add_argument("--transactions_only", action="store_true", help="Generate only transactions for the wallet")
    parser.add_argument("--wallet_only", action="store_true", help="Generate only the wallet object for the wallet")
    args = parser.parse_args()

    if args.transaction:
        if args.transactions_only or args.wallet_only:
            raise ValueError("The --transactions_only and --wallet_only flags are not allowed for transaction entries")

    if args.wallet:
        if args.transactions_only and args.wallet_only:
            raise ValueError("Cannot use --transactions_only and --wallet_only together")

    clear_directory("stix2_objects")

    fs_store = FileSystemStore("stix2_objects")
    
    # Download and store extension definitions
    extensions = download_extension_definitions()
    for key, ext_def in extensions.items():
        fs_store.add(stix2.parse(ext_def))

    stix_objects = []
    processed_wallets = set()

    if args.transaction:
        tx_data = get_transaction_data(args.transaction)
        wallets = set(inp["prev_out"]["addr"] for inp in tx_data["inputs"] if 'addr' in inp["prev_out"]) | set(out["addr"] for out in tx_data["out"] if 'addr' in out)
        wallet_objects = []
        for addr in wallets:
            if addr not in processed_wallets:
                wallet_object = create_wallet_object(addr)
                fs_store.add(stix2.parse(wallet_object))
                wallet_objects.append(wallet_object)
                processed_wallets.add(addr)
        stix_objects.extend(wallet_objects)
        transaction_object = create_transaction_object(tx_data)
        fs_store.add(stix2.parse(transaction_object))
        stix_objects.append(transaction_object)
    
    elif args.wallet:
        if args.wallet_only:
            wallet_object = create_wallet_object(args.wallet)
            fs_store.add(stix2.parse(wallet_object))
            stix_objects.append(wallet_object)
        else:
            wallet_data = get_wallet_data(args.wallet)
            if args.wallet not in processed_wallets:
                wallet_object = create_wallet_object(args.wallet)
                fs_store.add(stix2.parse(wallet_object))
                stix_objects.append(wallet_object)
                processed_wallets.add(args.wallet)
            for tx in wallet_data["txs"]:
                transaction_object = create_transaction_object(tx)
                fs_store.add(stix2.parse(transaction_object))
                stix_objects.append(transaction_object)
                if not args.transactions_only:
                    wallets = set(inp["prev_out"]["addr"] for inp in tx["inputs"] if 'addr' in inp["prev_out"]) | set(out["addr"] for out in tx["out"] if 'addr' in out)
                    wallet_objects = []
                    for addr in wallets:
                        if addr not in processed_wallets:
                            wallet_object = create_wallet_object(addr)
                            fs_store.add(stix2.parse(wallet_object))
                            wallet_objects.append(wallet_object)
                            processed_wallets.add(addr)
                    stix_objects.extend(wallet_objects)

    if stix_objects:
        stix_objects += list(extensions.values())
        sorted_stix_objects = sort_objects(stix_objects)
        stix_objects_str = json.dumps(sorted_stix_objects, sort_keys=True)
        bundle_id = str(uuid.uuid5(BUNDLE_NAMESPACE_UUID, md5(stix_objects_str.encode('utf-8')).hexdigest()))
        bundle = {
            "type": "bundle",
            "id": f"bundle--{bundle_id}",
            "objects": sorted_stix_objects
        }

        with open(f"stix2_objects/bundle--{bundle_id}.json", "w") as f:
            json.dump(bundle, f, indent=4)

if __name__ == "__main__":
    main()
