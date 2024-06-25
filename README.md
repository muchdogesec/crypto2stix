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
python3 crypto2stix.py --transaction HASH
```

Starting with a wallet hash;

```shell
python3 crypto2stix.py --wallet HASH --transactions_only
```

Passing the `--transactions_only` flag will generate the wallet for the wallet HASH passed in the CLI, and all transactions related to it.

Omitting the `--transactions_only` will also generate wallet objects for every single wallet mentioned in the transactions the wallet HASH passed in the CLI is linked to.

### Example runs using Wannacry data

```shell
python3 crypto2stix.py --transaction 3a5395bc3e8584786ad0598db33adda0b991814fd035089d69d7e2bda3272893
```

```shell
python3 crypto2stix.py --wallet 115p7UMMngoj1pMvkpHijcRdfJNXj6LrLn --transactions_only
```

```shell
python3 crypto2stix.py --wallet 115p7UMMngoj1pMvkpHijcRdfJNXj6LrLn
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
    "id": "cryptocurrency-transaction--1e832ccc-78e2-5be5-b004-18ed031b6efe",
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

```json
{
  "hash160": "00e8fd98ca34f195b020af4a8b1c7238663d4212",
  "address": "115p7UMMngoj1pMvkpHijcRdfJNXj6LrLn",
  "n_tx": 124,
  "n_unredeemed": 10,
  "total_received": 1487769994,
  "total_sent": 1441067602,
  "final_balance": 46702392,
  "txs": [
    {
      "hash": "14449446275da0bf11825d14733fcc28f7264f8a2c3a506752f92fddb8e1aa16",
      "ver": 1,
      "vin_sz": 1,
      "vout_sz": 22,
      "size": 880,
      "weight": 3520,
      "fee": 113880,
      "relayed_by": "0.0.0.0",
      "lock_time": 0,
      "tx_index": 797541991687679,
      "double_spend": false,
      "time": 1605337703,
      "block_index": 656858,
      "block_height": 656858,
      "inputs": [
        {
          "sequence": 4294967295,
          "witness": "",
          "script": "483045022100d2493ce331c957bc0b60cff36cebdc201cca7c70feaca5622a034a6377f63b5f02202976125322d2126737f4a3e8e2cf21efa2dd4e97a468c0b4292f3bd87fa10784012102ee5dc5bd7d0b31b6ff5012fc2f89d3795bec0eac2913ef3cdb72b3b6cfd332b7",
          "index": 0,
          "prev_out": {
            "type": 0,
            "spent": true,
            "value": 28527876087,
            "spending_outpoints": [
              {
                "tx_index": 797541991687679,
                "n": 0
              }
            ],
            "n": 5,
            "tx_index": 8651191654556922,
            "script": "76a914dba6d09a4cc20d8eb1c482c2e56b8d600fb9f58b88ac",
            "addr": "1M2QpWb7xspmtYHgVmGgrewWPBF7SjPCJb"
          }
        }
      ],
      "out": [
        {
          "type": 0,
          "spent": true,
          "value": 372891955,
          "spending_outpoints": [
            {
              "tx_index": 7076151901137692,
              "n": 1
            }
          ],
          "n": 0,
          "tx_index": 797541991687679,
          "script": "a91465fdc09b1cf60a82cbc9e059839fcc04ebf7f18487",
          "addr": "3AzJ9wbhhDsfCvWGU74uWFSQ2E8hWaTq5C"
        },
        {
          "type": 0,
          "spent": true,
          "value": 2767591,
          "spending_outpoints": [
            {
              "tx_index": 8005882464485736,
              "n": 17
            }
          ],
          "n": 1,
          "tx_index": 797541991687679,
          "script": "76a9144964d8fc9049f1953a125e1e387987b26fa7c99a88ac",
          "addr": "17h5923U88esSwtmJa4v1EgVW9vi1dJX1q"
        },
        {
          "type": 0,
          "spent": true,
          "value": 8432592,
          "spending_outpoints": [
            {
              "tx_index": 1624767403743273,
              "n": 20
            }
          ],
          "n": 2,
          "tx_index": 797541991687679,
          "script": "76a9142a512d273bb2d7ed97d86958a694b4838dff2f3888ac",
          "addr": "14rkdHrh1E3L34v9vTevoJ5hGfLmM2eLTX"
        },
        {
          "type": 0,
          "spent": true,
          "value": 9409489,
          "spending_outpoints": [
            {
              "tx_index": 1369064840368594,
              "n": 8
            }
          ],
          "n": 3,
          "tx_index": 797541991687679,
          "script": "76a9142a512d273bb2d7ed97d86958a694b4838dff2f3888ac",
          "addr": "14rkdHrh1E3L34v9vTevoJ5hGfLmM2eLTX"
        },
        {
          "type": 0,
          "spent": true,
          "value": 3660000,
          "spending_outpoints": [
            {
              "tx_index": 2573651081540839,
              "n": 18
            }
          ],
          "n": 4,
          "tx_index": 797541991687679,
          "script": "a91461b2c86be4d3a90e703f39e49e8027f796388e7587",
          "addr": "3AbbeCpuxNk1Ceq16tM1Np6fUXJjAqdFMk"
        },
        {
          "type": 0,
          "spent": true,
          "value": 11925214,
          "spending_outpoints": [
            {
              "tx_index": 504512970446827,
              "n": 5
            }
          ],
          "n": 5,
          "tx_index": 797541991687679,
          "script": "a9144ad58e8e463e57758d03f0e1254e7e235015ef4d87",
          "addr": "38WhkvtJUeMtoqAb7SJKtjWYGf8YvT4hLC"
        },
        {
          "type": 0,
          "spent": true,
          "value": 17301260,
          "spending_outpoints": [
            {
              "tx_index": 2821858673363502,
              "n": 46
            }
          ],
          "n": 6,
          "tx_index": 797541991687679,
          "script": "a9145657264a8e100788dbcb0946c0d2a0256024cab087",
          "addr": "39ZYSJLoCAKCDyavynjzXG7VSTeqmh3AXW"
        },
        {
          "type": 0,
          "spent": true,
          "value": 240937162,
          "spending_outpoints": [
            {
              "tx_index": 778137703303881,
              "n": 2
            }
          ],
          "n": 7,
          "tx_index": 797541991687679,
          "script": "a914c3597834267dc19cc477e023730eae6771a8e34f87",
          "addr": "3KVvsQNKaTvTE7gGuWpVZfVEPYt5Kn5QvK"
        },
        {
          "type": 0,
          "spent": true,
          "value": 154285425,
          "spending_outpoints": [
            {
              "tx_index": 959021266784189,
              "n": 19
            }
          ],
          "n": 8,
          "tx_index": 797541991687679,
          "script": "a91408e8f6a46f317646861d87f846e957ffcd7710ac87",
          "addr": "32W8QfNgcK32hBRTm6QAgQP7A7j9817JZY"
        },
        {
          "type": 0,
          "spent": true,
          "value": 259666,
          "spending_outpoints": [
            {
              "tx_index": 8849451891187253,
              "n": 2
            }
          ],
          "n": 9,
          "tx_index": 797541991687679,
          "script": "a91463a7dddfde93cfcba03a26e3a601a623bbcb5ad887",
          "addr": "3Amwv7mjzuUyRarogoB6epED9NNobbj3VT"
        },
        {
          "type": 0,
          "spent": false,
          "value": 3720000,
          "spending_outpoints": [],
          "n": 10,
          "tx_index": 797541991687679,
          "script": "76a91400e8fd98ca34f195b020af4a8b1c7238663d421288ac",
          "addr": "115p7UMMngoj1pMvkpHijcRdfJNXj6LrLn"
        },
        {
          "type": 0,
          "spent": true,
          "value": 1842500,
          "spending_outpoints": [
            {
              "tx_index": 8892224564038889,
              "n": 8
            }
          ],
          "n": 11,
          "tx_index": 797541991687679,
          "script": "a9147a1fceff4f6d5a6a5b761668b1a7f7d2fb3569e087",
          "addr": "3CpkU3dabLuXeoof1o4ZhiJ4bzCTSu631s"
        },
        {
          "type": 0,
          "spent": true,
          "value": 89827000,
          "spending_outpoints": [
            {
              "tx_index": 7283568728571289,
              "n": 0
            }
          ],
          "n": 12,
          "tx_index": 797541991687679,
          "script": "76a914ca85e0b001b949837563b49d4a153286ef08b31888ac",
          "addr": "1KTqsjbarRhcYgmPMrVLPeKBvqk4vXSY9U"
        },
        {
          "type": 0,
          "spent": false,
          "value": 24950000,
          "spending_outpoints": [],
          "n": 13,
          "tx_index": 797541991687679,
          "script": "76a914e7856d810f7fe2b0f2c0d7ea806786a1cbda6bff88ac",
          "addr": "1N7Aw34J8ih6LSTMWHHSpEdKyFwYgSQZRF"
        },
        {
          "type": 0,
          "spent": true,
          "value": 850000,
          "spending_outpoints": [
            {
              "tx_index": 61226390326379,
              "n": 0
            }
          ],
          "n": 14,
          "tx_index": 797541991687679,
          "script": "a914c513776ea505b4b90670469315ecc97da63ed4fd87",
          "addr": "3Kf4MtjKCna38MzDousEEo83KeMLfkjjDE"
        },
        {
          "type": 0,
          "spent": true,
          "value": 4000000,
          "spending_outpoints": [
            {
              "tx_index": 8575415627799691,
              "n": 0
            }
          ],
          "n": 15,
          "tx_index": 797541991687679,
          "script": "a9142eff3785c47ea7595261bfe0cccb4da1e75f1dc987",
          "addr": "35yWk9Y6WSE8jXyFuFYiFW6idndxDnid32"
        },
        {
          "type": 0,
          "spent": true,
          "value": 320300,
          "spending_outpoints": [
            {
              "tx_index": 948844641953240,
              "n": 307
            }
          ],
          "n": 16,
          "tx_index": 797541991687679,
          "script": "76a914897d50274eb9f41bc600541ab87223d96013c7c588ac",
          "addr": "1DXyhBt2g7gBx6xvmqkBTyuxwg8BpJgF9e"
        },
        {
          "type": 0,
          "spent": true,
          "value": 3660000,
          "spending_outpoints": [
            {
              "tx_index": 5787612263125314,
              "n": 45
            }
          ],
          "n": 17,
          "tx_index": 797541991687679,
          "script": "a9140125222e5f86b1928a02443c855059a071838c3387",
          "addr": "31o55pPJnveAzEesUeGzZorfoiXnVkqVPo"
        },
        {
          "type": 0,
          "spent": true,
          "value": 7726400,
          "spending_outpoints": [
            {
              "tx_index": 6118670735117055,
              "n": 0
            }
          ],
          "n": 18,
          "tx_index": 797541991687679,
          "script": "76a914d897d4101b9aca38b6e9503a89c6464689a5316c88ac",
          "addr": "1LkEqf29URRxRRZ6xFveASFZFqVn1BtHMc"
        },
        {
          "type": 0,
          "spent": true,
          "value": 4650000,
          "spending_outpoints": [
            {
              "tx_index": 5345936843175744,
              "n": 12
            }
          ],
          "n": 19,
          "tx_index": 797541991687679,
          "script": "a9143c550f8cd26ee14c3a0f46b6024f8d498be9467687",
          "addr": "37C2NBFdq4XfQE3745fvy1NW23SPxQuFdQ"
        },
        {
          "type": 0,
          "spent": true,
          "value": 3660000,
          "spending_outpoints": [
            {
              "tx_index": 6062110509517792,
              "n": 3
            }
          ],
          "n": 20,
          "tx_index": 797541991687679,
          "script": "a9149cf1174ef27fa52111b6300d3311b423851db17587",
          "addr": "3Fzr9mZD1SM6wSt7jAFSjurNnMDFv8JuQF"
        },
        {
          "type": 0,
          "spent": true,
          "value": 27560685653,
          "spending_outpoints": [
            {
              "tx_index": 8135202909713236,
              "n": 0
            }
          ],
          "n": 21,
          "tx_index": 797541991687679,
          "script": "76a91473d45406e77a4a90edd3b103597bcfbafe211ef388ac",
          "addr": "1BZT4tJif1mdEBzoDALqJxguy2e3Mr8xzn"
        }
      ],
      "result": 3720000,
      "balance": 46702392
    },
```

_(response cut for brevity)._

This time the conversion is done in the same way as when starting with a transaction hash, the script simply uses the data inside the `txs` object.

The important logical difference here is that the same wallet ID could appear multiple times (as same wallet seen across multiple transactions).

## STIX2 Conversion

This script creates the STIX objects using the [stix2 Python Lib](https://stix2.readthedocs.io/en/latest/).

It utilises the filesystem store, which saves the output objects into a directory called `stix2_objects`. On each script run this directory is deleted and then recreated with new objects.

All the generated objects are placed into a STIX bundle in the `stix2_objects` directory.

```json
{
    "type": "bundle",
    "id": "bundle--<UUIDV5>",
    "objects": [
        "ALL STIX OBJECTS CREATED"
    ]
}
```

The UUID is generated using the namespace `63340903-e6fa-46e4-a5e7-25c1523ca345` and the md5 hash of all objects sorted in the bundle.

The bundle file is also names in the format `bundle--<UUIDV5>.json`.

## Useful supporting tools

* To generate STIX 2.1 Objects: [stix2 Python Lib](https://stix2.readthedocs.io/en/latest/)
* The STIX 2.1 specification: [STIX 2.1 docs](https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html)
* [Blockchain API](https://www.blockchain.com/explorer/api/blockchain_api)

## Support

[Minimal support provided via the DOGESEC community](https://community.dogesec.com/).

## License

[Apache 2.0](/LICENSE).