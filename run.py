from flask import Flask, render_template, request, redirect, url_for, session, jsonify, abort
from apscheduler.schedulers.background import BackgroundScheduler
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secret key for session management

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Available tickets (hard coded)
available_tickets = {
    'ticket1': {
        'name': 'Concert Ticket',
        'price': 50,
        'quantity': 10,
        'time': '7:00 PM',
        'place': 'Concert Hall',
        'grade': 'VIP'
    },
    'ticket2': {
        'name': 'Movie Ticket',
        'price': 15,
        'quantity': 20,
        'time': '3:00 PM',
        'place': 'Cinema',
        'grade': 'Standard'
    },
    'ticket3': {
        'name': 'Sports Ticket',
        'price': 30,
        'quantity': 5,
        'time': '2:30 PM',
        'place': 'Stadium',
        'grade': 'Premium'
    },
  # add more tickets if requried
}

# Data structure to store booked tickets, user balances, and pending transactions (hard coded)
booked_tickets = {}
user_data = {
    'user1': {
        'id': 'user1',
        'password': 'password1',
        'kyc': 'kyc_info1',
        'owned_tickets': {},
        'balance': 100
    },
    'user2': {
        'id': 'user2',
        'password': 'password2',
        'kyc': 'kyc_info2',
        'owned_tickets': {},
        'balance': 150
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
scheduler.add_job(process_daily_tasks, 'cron', hour=0, minute=0, second=0)

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
        
        if action == 'book':
            if quantity <= available_tickets[ticket_id]['quantity'] and quantity <= user_info['balance']:
                # Execute the booking transaction
                booked_tickets.setdefault(ticket_id, {'quantity': 0})
                booked_tickets[ticket_id]['quantity'] += quantity
                available_tickets[ticket_id]['quantity'] -= quantity
                user_info['owned_tickets'].setdefault(ticket_id, 0)
                user_info['owned_tickets'][ticket_id] += quantity
                user_info['balance'] -= quantity * available_tickets[ticket_id]['price']
        elif action == 'cancel':
            if quantity <= user_info['owned_tickets'].get(ticket_id, 0):
                # Execute the cancellation transaction
                booked_tickets[ticket_id]['quantity'] -= quantity
                available_tickets[ticket_id]['quantity'] += quantity
                user_info['owned_tickets'][ticket_id] -= quantity
                user_info['balance'] += quantity * available_tickets[ticket_id]['price']

    # Clear the pending transactions after execution
    pending_transactions.clear()

# Routes

@app.route('/')
def index():
    if 'username' in session:
    username = session['username']
    user_info = user_data.get(username, None)

    if user_info:
        return render_template('index.html', available_tickets=available_tickets, user_info=user_info, pending_transactions=list(pending_transactions))
    else:
        abort(404, description="User not found in user_data")
else:
    user_info = None  # Set user_info to None if the user is not logged in
    return render_template('index.html', available_tickets=available_tickets, user_info=user_info, pending_transactions=list(pending_transactions))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in user_data and user_data[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            abort(401)  # Unauthorized
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/book/<ticket_id>', methods=['POST'])
def book_ticket(ticket_id):
    if 'username' in session:
        if ticket_id in available_tickets:
            quantity_requested = int(request.form.get('quantity', 1))
            user_info = user_data[session['username']]
            user_balance = user_info['balance']

            total_cost = quantity_requested * available_tickets[ticket_id]['price']

            if total_cost > user_balance:
                abort(400, description="Not enough balance to book the tickets")

            if quantity_requested > available_tickets[ticket_id]['quantity']:
                abort(400, description="Not enough tickets available")

            if ticket_id not in booked_tickets:
                booked_tickets[ticket_id] = {'quantity': 0}

            booked_tickets[ticket_id]['quantity'] += quantity_requested
            available_tickets[ticket_id]['quantity'] -= quantity_requested

            user_info['tickets'].setdefault(ticket_id, 0)
            user_info['tickets'][ticket_id] += quantity_requested

            user_info['balance'] = user_balance - total_cost

            # Add the booking transaction to the pending transactions set
            pending_transactions.add((ticket_id, session['username'], 'book', quantity_requested))

            return jsonify(message="Ticket booked successfully")
        else:
            abort(404, description="Ticket not found")
    else:
        abort(401)  # Unauthorized

@app.route('/cancel/<ticket_id>', methods=['POST'])
def cancel_ticket(ticket_id):
    if 'username' in session:
        if ticket_id in user_data[session['username']]['tickets']:
            quantity_requested = int(request.form.get('quantity', 1))

            if quantity_requested > user_data[session['username']]['tickets'][ticket_id]:
                abort(400, description="Cannot cancel more tickets than owned")

            booked_tickets[ticket_id]['quantity'] -= quantity_requested
            available_tickets[ticket_id]['quantity'] += quantity_requested

            user_data[session['username']]['tickets'][ticket_id] -= quantity_requested
            user_data[session['username']]['balance'] += quantity_requested * available_tickets[ticket_id]['price']

            # Add the cancellation transaction to the pending transactions set
            pending_transactions.add((ticket_id, session['username'], 'cancel', quantity_requested))

            return jsonify(message="Ticket canceled successfully")
        else:
            abort(404, description="Ticket not found in your bookings")
    else:
        abort(401)  # Unauthorized

@app.route('/add_balance', methods=['POST'])
def add_balance():
    if 'username' in session:
        user_info = user_data[session['username']]
        amount = int(request.form.get('amount', 0))

        if amount > 0:
            user_info['balance'] += amount

        return jsonify(message="Balance added successfully")
    else:
        abort(401)  # Unauthorized

@app.route('/withdraw_balance', methods=['POST'])
def withdraw_balance():
    if 'username' in session:
        user_info = user_data[session['username']]
        amount = int(request.form.get('amount', 0))

        if amount <= 0:
            abort(400, description="Invalid amount for withdrawal")

        if amount <= user_info['balance']:
            # Process withdrawal
            user_info['balance'] -= amount

            # You can add additional logic here, such as sending the withdrawal to a bank account, etc.

            return jsonify(message="Withdrawal successful")
        else:
            abort(400, description="Not enough balance for withdrawal")
    else:
        abort(401)  # Unauthorized

if __name__ == '__main__':
    app.run(debug=True)
