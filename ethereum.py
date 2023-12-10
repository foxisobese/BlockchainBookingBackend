from web3 import Web3

def connect_to_ethereum(node_endpoint):
    web3 = Web3(Web3.HTTPProvider(node_endpoint))
    if web3.is_connected():
        print("Connected to Ethereum node")
    else:
        print("Connection failed")
    return web3

def transfer_tokens(web3, instance, sender_address, receiver_address, token_ID):

    transaction = instance.functions.transferFrom(sender_address,receiver_address,token_ID).buildTransaction({
    'gas': 200000,
    'gasPrice': web3.toWei('50', 'gwei'),  # Replace with your desired gas price
    'nonce': web3.eth.getTransactionCount(sender_address),
    })

    private_key='bf7529166eb734e57fbdb5d63fcccc052627460a63cc4ad90db6bd867c2760c3'

    # Sign the transaction
    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)

    # Send the transaction
    transaction_hash = web3.eth.sendRawTransaction(signed_transaction.rawTransaction)

    print(f"Transaction Hash: {transaction_hash}")


def transfer_tickets(web3,instance, address, token_ID, amount):

    transaction = instance.functions.transferTicket(address,token_ID,amount).buildTransaction({
    'gas': 200000,
    'gasPrice': web3.toWei('50', 'gwei'),  # Replace with your desired gas price
    'nonce': web3.eth.getTransactionCount(address),
    })

    private_key='bf7529166eb734e57fbdb5d63fcccc052627460a63cc4ad90db6bd867c2760c3'

    # Sign the transaction
    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)

    # Send the transaction
    transaction_hash = web3.eth.sendRawTransaction(signed_transaction.rawTransaction)

    print(f"Transaction Hash: {transaction_hash}")

def mint_tickets(web3,instance, event_name, event_date, seat_number, price, new_token_url):
    pass # not sure what to designate in nonce value...
