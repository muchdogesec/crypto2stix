# crypto2stix

A command line tool that takes a crypto transactions or wallets and turns them into STIX objects. Currently only support Bitcoin.

## Overview

One of our tools, [txt2stix](https://github.com/muchdogesec/txt2stix/), extracts bitcoin wallets from text.

Behind each wallet (and transaction) is wide variety of data.

Given the main use-cases of txt2stix is for threat intelligence research, this data can be incredibly useful (e.g. what transactions has a wallet had inflows?).

crypto2stix is designed to take a crypto transaction or wallet hash, enrich them with more data, and convert everything into STIX objects.

## Installing the script

To install crypto2stix;

```shell
# clone the latest code
git clone https://github.com/muchdogesec/crypto2stix
# create a venv
cd crypto2stix
python3 -m venv crypto2stix-venv
source crypto2stix-venv/bin/activate
# install requirements
pip3 install -r requirements.txt
```

## Running the script

Starting with a transaction hash;

```shell
python3 crypto2stix.py --transaction ID
```

Starting with a wallet hash;

```shell
python3 crypto2stix.py --wallet ID
```

## Blockchain data

The [blockchain.com API] is a good resource for looking up Bitcoin transactions and wallets.

### Starting with a transaction

```shell
GET https://blockchain.info/rawtx/$tx_hash
```

```shell
GET https://blockchain.info/rawtx/d63a3757a2a7b4c58e49f5a2e4236b1d4cbc2e4ffc9aa04c636707cb0bbbee7b
```

```json
{
  "hash": "d63a3757a2a7b4c58e49f5a2e4236b1d4cbc2e4ffc9aa04c636707cb0bbbee7b",
  "ver": 1,
  "vin_sz": 2,
  "vout_sz": 2,
  "size": 373,
  "weight": 1492,
  "fee": 50000,
  "relayed_by": "0.0.0.0",
  "lock_time": 0,
  "tx_index": 4360488657445100,
  "double_spend": false,
  "time": 1495108523,
  "block_index": 466967,
  "block_height": 466967,
  "inputs": [
    {
      "sequence": 4294967295,
      "witness": "",
      "script": "483045022100b107ae12209e86cee676940436f6778bc29d54a0e4047f1b367c10959f61a0fb022045ce67f745f67f6d4033216eb0e5d78549db675abbb0bdf4e257700ea68394ad012102b0eb710c74a391c8e964d72b3361871d25191c87f1c9a8e42f7ee79bbf2bda49",
      "index": 0,
      "prev_out": {
        "type": 0,
        "spent": true,
        "value": 11845608,
        "spending_outpoints": [
          {
            "tx_index": 4360488657445100,
            "n": 0
          }
        ],
        "n": 1,
        "tx_index": 4021013296723384,
        "script": "76a914b514578153fa240bfc568d6d042335914c50ab4d88ac",
        "addr": "1HWTg6YPnbb4DoPqmY8bwFr6s8BoHyAVBf"
      }
    },
    {
      "sequence": 4294967295,
      "witness": "",
      "script": "4730440220440d8f90d0feb3a795122a38f24904103abe47620b0c83eca96de616015a93e002205afc3099b5e7cd4b93add77496be979c3263842dd15a669b5deacbfbfe48b249012102c9161829e8e774355f09b5fe0b7a0227076d7d843bcace78cf4dd275aceaf368",
      "index": 1,
      "prev_out": {
        "type": 0,
        "spent": true,
        "value": 5464724,
        "spending_outpoints": [
          {
            "tx_index": 4360488657445100,
            "n": 1
          }
        ],
        "n": 1,
        "tx_index": 5454612254876663,
        "script": "76a914d4a013f66ea64c5a7535626ed7d740834bfcb1a488ac",
        "addr": "1LPG25hYrc91YgoBqrZwkqg7xapLX5GQGe"
      }
    }
  ],
  "out": [
    {
      "type": 0,
      "spent": true,
      "value": 17171661,
      "spending_outpoints": [
        {
          "tx_index": 1682140634081877,
          "n": 62
        }
      ],
      "n": 0,
      "tx_index": 4360488657445100,
      "script": "76a91400e8fd98ca34f195b020af4a8b1c7238663d421288ac",
      "addr": "115p7UMMngoj1pMvkpHijcRdfJNXj6LrLn"
    },
    {
      "type": 0,
      "spent": false,
      "value": 88671,
      "spending_outpoints": [],
      "n": 1,
      "tx_index": 4360488657445100,
      "script": "76a9149872ea5a955b2148b2092d4b5934cdb91c70efb188ac",
      "addr": "1Eu5Nd9mx3qXn52gKy7zTQRvgXcHeQCfwa"
    }
  ]
}
```

The transaction `time` is `1495108523` (epoch time) = `2017-05-18T11:53:23.000Z`.

The `fee` was `50000` = `0.0005` BTC.

The block ID was `466967`

The transaction has two `inputs.prev_out` entries (the wallets the Bitcoin came from) with `addr` and `value` properties:

* `1HWTg6YPnbb4DoPqmY8bwFr6s8BoHyAVBf` who sent `11845608` = (11845608 / 100000000) `0.11845608` BTC)
* `1LPG25hYrc91YgoBqrZwkqg7xapLX5GQGe` who sent `5464724` = `0.05464724` BTC

They send money to the `out` entries;

* `115p7UMMngoj1pMvkpHijcRdfJNXj6LrLn` who received `17171661` = `0.17171661` BTC
* `1Eu5Nd9mx3qXn52gKy7zTQRvgXcHeQCfwa` who received `88671` = `0.00088671` BTC

Using our custom STIX objects:

* cryptocurrency-transaction
    * extension-definition
* cryptocurrency-wallet
    * extension-definition

It is possible to model this transaction.

The wallets;

```json
{
    "type": "cryptocurrency-wallet",
    "spec_version": "2.1",
    "id": "cryptocurrency-wallet--02095d7d-fc71-5aee-8037-a0baeefc8356",
    "address": "1HWTg6YPnbb4DoPqmY8bwFr6s8BoHyAVBf",
    "extensions": {
        "extension-definition--be78509e-6958-51b1-8b26-d17ee0eba2d7": {
            "extension_type": "new-sco"
        }
    }
},
{
    "type": "cryptocurrency-wallet",
    "spec_version": "2.1",
    "id": "cryptocurrency-wallet--f6b10c0c-745f-580b-89e0-616971d2b75d",
    "address": "1LPG25hYrc91YgoBqrZwkqg7xapLX5GQGe",
    "extensions": {
        "extension-definition--be78509e-6958-51b1-8b26-d17ee0eba2d7": {
            "extension_type": "new-sco"
        }
    }
},
{
    "type": "cryptocurrency-wallet",
    "spec_version": "2.1",
    "id": "cryptocurrency-wallet--445cd431-5735-5436-9713-8798a63c1952",
    "address": "115p7UMMngoj1pMvkpHijcRdfJNXj6LrLn",
    "extensions": {
        "extension-definition--be78509e-6958-51b1-8b26-d17ee0eba2d7": {
            "extension_type": "new-sco"
        }
    }
},
{
    "type": "cryptocurrency-wallet",
    "spec_version": "2.1",
    "id": "cryptocurrency-wallet--76e4d830-ede6-5b40-817e-e42f06698970",
    "address": "1Eu5Nd9mx3qXn52gKy7zTQRvgXcHeQCfwa",
    "extensions": {
        "extension-definition--be78509e-6958-51b1-8b26-d17ee0eba2d7": {
            "extension_type": "new-sco"
        }
    }
}
```

The UUIDs are generated using the namespace `00abedb4-aa42-466c-9c01-fed23315a9b7` and the `address` value.

Now we can model the actual transaction using these objects.

```json
{
    "type": "cryptocurrency-transaction",
    "spec_version": "2.1",
    "id": "cryptocurrency-transaction--",
    "symbol": "BTC",
    "hash": "d63a3757a2a7b4c58e49f5a2e4236b1d4cbc2e4ffc9aa04c636707cb0bbbee7b",
    "block_id": "466967",
    "fee": "0.0005",
    "execution_time": "2017-05-18T11:53:23.000Z",
    "input": [
        {
            "address_ref": "cryptocurrency-wallet--02095d7d-fc71-5aee-8037-a0baeefc8356",
            "amount": 0.11845608
        },
        {
            "address_ref": "cryptocurrency-wallet--f6b10c0c-745f-580b-89e0-616971d2b75d",
            "amount": 0.05464724
        }
    ],
    "output": [
        {
            "address_ref": "cryptocurrency-wallet--445cd431-5735-5436-9713-8798a63c1952",
            "amount": 0.17171661
        },
        {
            "address_ref": "cryptocurrency-wallet--76e4d830-ede6-5b40-817e-e42f06698970",
            "amount": 0.00088671
        }
    ],
    "extensions": {
        "extension-definition--151d042d-4dcf-5e44-843f-1024440318e5": {
            "extension_type": "new-sco"
        }
    }
}
```

### Starting with a wallet



```shell
GET https://blockchain.info/rawaddr/$bitcoin_address
```

```shell
GET https://blockchain.info/rawaddr/115p7UMMngoj1pMvkpHijcRdfJNXj6LrLn
```



## Useful supporting tools

* To generate STIX 2.1 Objects: [stix2 Python Lib](https://stix2.readthedocs.io/en/latest/)
* The STIX 2.1 specification: [STIX 2.1 docs](https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html)
* [Blockchain API](https://www.blockchain.com/explorer/api/blockchain_api)

## Support

[Minimal support provided via the DOGESEC community](https://community.dogesec.com/).

## License

[Apache 2.0](/LICENSE).