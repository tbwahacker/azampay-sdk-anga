# AzamPay Python SDK for python developers (Pure/Native python, Django,Flask, FastApi et..c)

This SDK allows integration with AzamPay payment services.
whereby Initially the versions below 0.1.8 were only having MNO payments (Mobile Paymments) only. Much thanks to "Wadau" even Bank payments service is now working in released version 0.1.8 +

[![PyPI Downloads](https://static.pepy.tech/badge/azampay-sdk-anga/week)](https://pepy.tech/projects/azampay-sdk-anga)
[![PyPI Downloads](https://static.pepy.tech/badge/azampay-sdk-anga/month)](https://pepy.tech/projects/azampay-sdk-anga)
[![PyPI Downloads](https://static.pepy.tech/badge/azampay-sdk-anga)](https://pepy.tech/projects/azampay-sdk-anga)
![PyPI version](https://img.shields.io/pypi/v/azampay-sdk-anga)

<p align="start">
    <img src="/screenshots/azampay-logo.png" width="300" title="Azampay Logo" alt="Azampay Logo">
</p>

# ## Supported Banks

- Mpesa
- Airtel Money
- Halopesa
- Mix by yas
- Azampesa
- CRDB
- NMB


## Installation

```bash
pip install azampay-sdk-anga
```

## Usage
    try:
        # Generate a unique external ID
        external_id = str(uuid.uuid4())

        # Sample transaction details
        mobile_number = "0712345678"
        amount = 5000
        currency = "TZS"
        provider = "TIGO" # Mpesa, Airtel, Halotel, Azampesa, Tigo

        print("Initiating MNO Checkout...")
        response, ref = AzamPay.mno_checkout(  # For mobile payments
            mobile_number=mobile_number,
            amount=amount,
            currency=currency,
            provider=provider,
            external_id=external_id
        )

        print(f"Transaction Reference: {ref}")
        print("Response:")
        print(response)

    except Exception as e:
        print("Transaction failed:")
        print(str(e))
## So, what you have to do
is to create the callback(webhook) url (paste its path to azampay portal) and file in your project to accept and receive payment status && transactionId from Azampay

example callback_url.py (I will use flask for showcase) 'if status is rejected or success it will go update your payment/transaction database table. my example is ==> update_custom_o custom table'

```
from flask import Flask, request
from main import Main
from db import conn  # your DB connection file (pymysql or similar)

app = Flask(__name__)

@app.route('/callback', methods=['POST'])
def callback():
    if request.method != 'POST':
        return "Invalid method", 405

    try:
        main = Main(conn)
        data = request.get_json()
    except Exception:
        return "Server error", 500

    if not data or 'utilityref' not in data or 'transactionstatus' not in data:
        return "Invalid payload", 400

    utility_ref = data['utilityref']
    status = 'success' if data['transactionstatus'].lower() == 'success' else 'rejected'

    # Query and update transaction if it's still pending
    count, result = main.all_query_nolimit_s(
        'transactions',
        'AND status="pending" LIMIT 1',
        'reference',
        utility_ref
    )

    if count > 0:
        update = main.update_custom_o(
            'transactions', 'status', status, 'reference', utility_ref, 'AND status="pending"'
        )
        return "Transaction updated", 200
    else:
        return "Transaction not found", 404

```
## Optional 
Create a check.py (Elsewhere not in callback file) file to retrive your payment table and check if status has been changed, if yes or no then the redirect page will notify user as follows through the file 

templates/redirect.html
```
<!-- templates/redirect.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Transaction Status</title>
    <link href="{{ url_for('static', filename='bootstrap/css/bootstrap.min.css') }}" rel="stylesheet">
</head>
<body class="bg-light d-flex justify-content-center align-items-center" style="height: 100vh;">
    <div class="container text-center">
        {% if status == 'approved' %}
            <div class="alert alert-success shadow p-4 rounded" role="alert">
                <h1 class="mb-3">🎉 Transaction Approved</h1>
                <p class="lead">Your transaction was successfully completed.</p>
                <a href="/" class="btn btn-success mt-3">Go Home</a>
            </div>
        {% else %}
            <div class="alert alert-danger shadow p-4 rounded" role="alert">
                <h1 class="mb-3">❌ Transaction Failed</h1>
                <p class="lead">Sorry, something went wrong. Please try again.</p>
                <a href="/" class="btn btn-danger mt-3">Try Again</a>
            </div>
        {% endif %}
    </div>

    <script src="{{ url_for('static', filename='bootstrap/js/bootstrap.bundle.min.js') }}"></script>
</body>
</html>
```

## Remind you makesure that your .env in your root project folder must contains keys you got from azampay portal
```
AZAMPAY_ENVIRONMENT=sandbox  #production  (if u wanna change it to live then replace that sandbox to production)
AZAMPAY_APP_NAME=your-azam-app-name-here
AZAMPAY_CLIENT_ID=your-client-id-here
AZAMPAY_CLIENT_SECRET=your-secret-here
```
AzamPay Success Message Example
![AzamPay Success Message Example](screenshots/success_request.png)

## Credits and Inspiration
1. [Anganile Adam (Anga)](https://github.com/tbwahacker)
2. Thanks much to AzamPay for this support [Azampay Documentation](https://developerdocs.azampay.co.tz/redoc).
3. Tanzania Developers you are now free using the AzamPay python api
4. [All Contributors](../../contributors)

## Issues
Please open an issue here [**GITHUB**](https://github.com/tbwahacker/azampay-sdk-anga/)

## HAPPY ENJOY MAKING PAYMENTS. DON'T FORGET BUYING ME A ☕COFEE 😂😂😂
## 0685750593 / 0768571150 or gmail : twaloadam@gmail.com / anganileadam87@gmail.com

If you find this package useful, you can support us by starring this repository and sharing it with others.

## Licence
The MIT License (MIT).

## Contribute
""""  Feel Free to contribute by forking the Repo """"
