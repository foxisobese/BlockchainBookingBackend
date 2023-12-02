# BlockchainBookingBackend
backend application for blockchain based booking system using Flask

## Dependencies
```
pip install flask apscheduler
```
## Breif tour of the code

1. available_tickets, booked_tickets, user_data
Currently, availabe_tickets, booked_tickets and user_data are hard coded.
user_data can be accessed in index, after login.

ticket information includes:  name, price, quantitiy, time, place, grade
user data includes: id, password, kyc, owned tickets, balance

3. process_daily_tasks
Where booking-cancelling transactions requrests are met midnight, daily.
Currently, withdrawing the request is not implemented.

4. /login, /logout
UI should start from login page.
Currently, sign up is not implemented.

5. /
This is the index page where user information is displayed. (If loged in successfully)
Also, pending transactions (booking, cancelling) are displayed.

7. /book/<ticket_id>, /cancel/<ticket_id>
This is where booking and cancelling transactions are requested.
All requests has a chance to be executed at midnight, daily, undeterministically.

8. /add_balance, /withdraw_balance
Add or withdraw balance.
Currently, billing is not implemented.
   
