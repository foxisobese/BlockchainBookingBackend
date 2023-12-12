from app.ethereum import connect_to_ethereum, transfer_tokens
from flask import Flask, request, redirect, url_for, session, jsonify, abort
from apscheduler.schedulers.background import BackgroundScheduler
import random
import requests
from threading import Thread
from flask_cors import CORS
import logging

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secret key for session management
app.config["SERVER_NAME"] = "127.0.0.1:5000"
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_DOMAIN"] = "127.0.0.1:5000"
cors = CORS(app, supports_credentials=True)
logging.basicConfig(level=logging.INFO)
# logging.getLogger("web3.RequestManager").setLevel(logging.DEBUG)
# logging.getLogger("web3.providers.HTTPProvider").setLevel(logging.DEBUG)
# logging.getLogger("web3.RequestManager").propagate = True

node_endpoint = "https://arbitrum-goerli.publicnode.com"
web3 = connect_to_ethereum(node_endpoint)
digicket_abi = '[{"inputs":[{"internalType":"address","name":"initialOwner","type":"address"},{"internalType":"address","name":"_usdtAddress","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"address","name":"owner","type":"address"}],"name":"ERC721IncorrectOwner","type":"error"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ERC721InsufficientApproval","type":"error"},{"inputs":[{"internalType":"address","name":"approver","type":"address"}],"name":"ERC721InvalidApprover","type":"error"},{"inputs":[{"internalType":"address","name":"operator","type":"address"}],"name":"ERC721InvalidOperator","type":"error"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"ERC721InvalidOwner","type":"error"},{"inputs":[{"internalType":"address","name":"receiver","type":"address"}],"name":"ERC721InvalidReceiver","type":"error"},{"inputs":[{"internalType":"address","name":"sender","type":"address"}],"name":"ERC721InvalidSender","type":"error"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ERC721NonexistentToken","type":"error"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"OwnableInvalidOwner","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"OwnableUnauthorizedAccount","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"_fromTokenId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"_toTokenId","type":"uint256"}],"name":"BatchMetadataUpdate","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"MetadataUpdate","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"price","type":"uint256"}],"name":"TicketTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getTicketInfo","outputs":[{"components":[{"internalType":"string","name":"eventName","type":"string"},{"internalType":"string","name":"eventDate","type":"string"},{"internalType":"string","name":"seatNumber","type":"string"},{"internalType":"uint256","name":"price","type":"uint256"}],"internalType":"struct Digicket.TicketInfo","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"eventName","type":"string"},{"internalType":"string","name":"eventDate","type":"string"},{"internalType":"string","name":"seatNumber","type":"string"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"string","name":"newTokenURI","type":"string"}],"name":"mintTicket","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"tokenCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256","name":"usdtAmount","type":"uint256"}],"name":"transferTicket","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"usdt","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'
digicket_address = web3.to_checksum_address(
    "0x53933c4a96F8DbFCbdB04916767F788c38bD4401"
)
instance = web3.eth.contract(address=digicket_address, abi=digicket_abi)


# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Available tickets (hard coded)
available_tickets = {
    "ticket1": {
        "name": "Concert Ticket",
        "price": 50,
        "quantity": 10,
        "time": "7:00 PM",
        "place": "Concert Hall",
        "grade": "VIP",
    },
    "ticket2": {
        "name": "Movie Ticket",
        "price": 15,
        "quantity": 20,
        "time": "3:00 PM",
        "place": "Cinema",
        "grade": "Standard",
    },
    "ticket3": {
        "name": "Sports Ticket",
        "price": 30,
        "quantity": 5,
        "time": "2:30 PM",
        "place": "Stadium",
        "grade": "Premium",
    },
    # add more tickets if requried
}

# Data structure to store booked tickets, user balances, and pending transactions (hard coded)
booked_tickets = {}
user_data = {
    "admin": {
        "id": "admin",
        "password": "password0",
        "kyc": "kyc_info0",
        "owned_tickets": {},
        "balance": 10000,
        "address": "0x4f8cf2c649b309477b31a28c3e4ffa4bd3378831",
    },
    "user1": {
        "id": "user1",
        "password": "password1",
        "kyc": "kyc_info1",
        "owned_tickets": {},
        "balance": 100,
        "address": "0x4f8cf2c649b309477b31a28c3e4ffa4bd3378831",
    },
    "user2": {
        "id": "user2",
        "password": "password2",
        "kyc": "kyc_info2",
        "owned_tickets": {},
        "balance": 150,
        "address": "0x4f8cf2c649b309477b31a28c3e4ffa4bd3378831",
    },
    # Add more users if required
}

pending_transactions = set()


def process_daily_tasks():
    """
    Function to be executed daily at midnight to process ticket exchanges/purchases.
    """
    print("Processing daily tasks at midnight...")

    # Step 1: Collect and consolidate pending transactions
    # For simplicity, we use a set to represent pending transactions
    global pending_transactions
    all_pending_transactions = list(pending_transactions)

    # Step 2: Execute transactions
    execute_transactions(all_pending_transactions)


# Schedule the daily task at midnight
scheduler.add_job(process_daily_tasks, "cron", hour=0, minute=0, second=0)


def execute_transactions(all_pending_transactions):
    """
    Simple logic to execute transactions.
    Matches same number of booking and cancelling from shuffled requests.
    """
    global booked_tickets, user_data

    # Shuffle the list of pending transactions to randomize the matching
    random.shuffle(all_pending_transactions)

    for transaction in all_pending_transactions:
        ticket_id, user_id, action, quantity = transaction
        user_info = user_data[user_id]
        total_cost = quantity * available_tickets[ticket_id]["price"]

        # Use the admin user's address as the destination
        destination_address = user_data["admin"]["address"]

        if action == "book":
            if (
                quantity <= available_tickets[ticket_id]["quantity"]
                and total_cost <= user_info["balance"]
            ):
                # Execute the booking transaction
                booked_tickets.setdefault(ticket_id, {"quantity": 0})
                booked_tickets[ticket_id]["quantity"] += quantity
                available_tickets[ticket_id]["quantity"] -= quantity
                user_info["owned_tickets"].setdefault(ticket_id, 0)
                user_info["owned_tickets"][ticket_id] += quantity
                user_info["balance"] -= quantity * available_tickets[ticket_id]["price"]

                transfer_tokens(
                    web3, instance, user_info["address"], destination_address, 1
                )
        elif action == "cancel":
            if quantity <= user_info["owned_tickets"].get(ticket_id, 0):
                # Execute the cancellation transaction
                booked_tickets[ticket_id]["quantity"] -= quantity
                available_tickets[ticket_id]["quantity"] += quantity
                user_info["owned_tickets"][ticket_id] -= quantity
                user_info["balance"] += quantity * available_tickets[ticket_id]["price"]

                transfer_tokens_data = {
                    "from": destination_address,
                    "to": user_info["address"],
                    "tokenid": ticket_id,
                }
                transfer_tokens_response = requests.post(
                    "http://blockchain-app-host:port/transfer_tokens",
                    json=transfer_tokens_data,
                )

    # Clear the pending transactions after execution
    pending_transactions.clear()


# Routes


@app.route("/")
def index():
    if "username" in session:
        username = session.get("username", "user1")
        user_info = user_data.get(username, None)

        if user_info:
            return jsonify(
                available_tickets=available_tickets,
                user_info=user_info,
                pending_transactions=list(pending_transactions),
            )
        else:
            abort(404, description="User not found in user_data")
    else:
        user_info = None  # Set user_info to None if the user is not logged in
        return jsonify(
            available_tickets=available_tickets,
            user_info=user_info,
            pending_transactions=list(pending_transactions),
        )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in user_data and user_data[username]["password"] == password:
            session["username"] = username
            return redirect(url_for("index"))
        else:
            abort(401)  # Unauthorized
    return jsonify("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


@app.route("/book/<ticket_id>", methods=["POST"])
def book_ticket(ticket_id):
    if ticket_id in available_tickets:
        quantity_requested = int(request.form.get("quantity", 1))
        user_info = user_data[session.get("username", "user1")]
        user_balance = user_info["balance"]

        total_cost = quantity_requested * available_tickets[ticket_id]["price"]

        if total_cost > user_balance:
            abort(400, description="Not enough balance to book the tickets")

        if quantity_requested > available_tickets[ticket_id]["quantity"]:
            abort(400, description="Not enough tickets available")

        if ticket_id not in booked_tickets:
            booked_tickets[ticket_id] = {"quantity": 0}

        booked_tickets[ticket_id]["quantity"] += quantity_requested
        available_tickets[ticket_id]["quantity"] -= quantity_requested

        user_info["owned_tickets"].setdefault(ticket_id, 0)
        user_info["owned_tickets"][ticket_id] += quantity_requested

        user_info["balance"] = user_balance - total_cost

        # Add the booking transaction to the pending transactions set
        pending_transactions.add(
            (ticket_id, session.get("username", "user1"), "book", quantity_requested)
        )

        Thread(target=process_daily_tasks).run()

        return jsonify(message="Ticket booked successfully")
    else:
        abort(404, description="Ticket not found")


@app.route("/cancel/<ticket_id>", methods=["POST"])
def cancel_ticket(ticket_id):
    if ticket_id in user_data[session.get("username", "user1")]["owned_tickets"]:
        quantity_requested = int(request.form.get("quantity", 1))

        if (
            quantity_requested
            > user_data[session.get("username", "user1")]["owned_tickets"][ticket_id]
        ):
            abort(400, description="Cannot cancel more tickets than owned")

        booked_tickets[ticket_id]["quantity"] -= quantity_requested
        available_tickets[ticket_id]["quantity"] += quantity_requested

        user_data[session.get("username", "user1")]["owned_tickets"][
            ticket_id
        ] -= quantity_requested
        user_data[session.get("username", "user1")]["balance"] += (
            quantity_requested * available_tickets[ticket_id]["price"]
        )

        # Add the cancellation transaction to the pending transactions set
        pending_transactions.add(
            (ticket_id, session.get("username", "user1"), "cancel", quantity_requested)
        )

        return jsonify(message="Ticket canceled successfully")
    else:
        abort(404, description="Ticket not found in your bookings")


@app.route("/add_balance", methods=["POST"])
def add_balance():
    user_info = user_data[session.get("username", "user1")]
    amount = int(request.form.get("amount", 0))

    if amount > 0:
        user_info["balance"] += amount

    return jsonify(message="Balance added successfully")


@app.route("/withdraw_balance", methods=["POST"])
def withdraw_balance():
    user_info = user_data[session.get("username", "user1")]
    amount = int(request.form.get("amount", 0))

    if amount <= 0:
        abort(400, description="Invalid amount for withdrawal")

    if amount <= user_info["balance"]:
        # Process withdrawal
        user_info["balance"] -= amount

        # You can add additional logic here, such as sending the withdrawal to a bank account, etc.

        return jsonify(message="Withdrawal successful")
    else:
        abort(400, description="Not enough balance for withdrawal")


if __name__ == "__main__":
    app.run(debug=True)
