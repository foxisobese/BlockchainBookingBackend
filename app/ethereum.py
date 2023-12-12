from web3 import Web3


def connect_to_ethereum(node_endpoint):
    web3 = Web3(Web3.HTTPProvider(node_endpoint))
    if web3.is_connected():
        print("Connected to Ethereum node")
        print(f"chainID:{web3.eth.chain_id}")
    else:
        print("Connection failed")
    return web3


def transfer_tokens(web3, instance, sender_address, receiver_address, token_ID):
    sender_address = web3.to_checksum_address(sender_address)
    receiver_address = web3.to_checksum_address(receiver_address)
    private_key = "bf7529166eb734e57fbdb5d63fcccc052627460a63cc4ad90db6bd867c2760c3"

    transaction = instance.functions.transferFrom(
        sender_address, receiver_address, token_ID
    ).build_transaction(
        {
            "gas": 200000,
            "gasPrice": web3.eth.gas_price,
            "nonce": web3.eth.get_transaction_count(
                web3.eth.account.from_key(private_key).address
            ),
        }
    )

    # Sign the transaction
    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)

    # Send the transaction
    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

    print(f"Transaction Hash: {transaction_hash.hex()}")

    print(web3.eth.get_transaction_receipt(transaction_hash))


def transfer_tickets(web3, instance, address, token_ID, amount):
    address = web3.to_checksum_address(address)
    private_key = "bf7529166eb734e57fbdb5d63fcccc052627460a63cc4ad90db6bd867c2760c3"
    transaction = instance.functions.transferTicket(
        address, token_ID, amount
    ).build_transaction(
        {
            "gas": 200000,
            "gasPrice": int(web3.eth.gas_price * 1.1),
            "nonce": web3.eth.get_transaction_count(
                web3.eth.account.from_key(private_key).address
            ),
        }
    )

    # Sign the transaction
    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)

    # Send the transaction
    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    web3.eth.wait_for_transaction_receipt(transaction_hash)
    print(f"Transaction Hash: {transaction_hash.hex()}")


def mint_tickets(
    web3, instance, event_name, event_date, seat_number, price, new_token_url
):
    pass  # not sure what to designate in nonce value...
