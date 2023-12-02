# BlockchainBookingBackend
backend application for blockchain based booking system using Flask

## Dependencies
```
pip install flask apscheduler
```
## Breif tour of the code

* available_tickets, booked_tickets, user_data

Currently, availabe_tickets, booked_tickets and user_data are hard coded.
user_data can be accessed in index, after login.

ticket information includes:  name, price, quantitiy, time, place, grade

user data includes: id, password, kyc, owned tickets, balance

* process_daily_tasks

Where booking-cancelling transactions requrests are met midnight, daily.

Currently, withdrawing the request is not implemented.

* /login, /logout

UI should start from login page.

Currently, sign up is not implemented.

* /

This is the index page where user information is displayed. (If loged in successfully)

Also, pending transactions (booking, cancelling) are displayed.

* /book/<ticket_id>, /cancel/<ticket_id>

This is where booking and cancelling transactions are requested.

All requests has a chance to be executed at midnight, daily, undeterministically.

* /add_balance, /withdraw_balance

Add or withdraw balance.

Currently, billing is not implemented.
   
