# azampay.py (or azampay/core.py if split)
import requests
from azampay.config import Config
from azampay.exceptions import AuthenticationError, EnvironmentError

config = Config()  # Create config instance

class AzamPay:
    @staticmethod
    def get_env_urls():
        if config.ENVIRONMENT == "production":
            auth_url = "https://authenticator.azampay.co.tz"
            checkout_url = "https://checkout.azampay.co.tz"
        else:
            auth_url = "https://authenticator-sandbox.azampay.co.tz"
            checkout_url = "https://sandbox.azampay.co.tz"

        return {"auth_url": auth_url, "checkout_url": checkout_url}

    @staticmethod
    def get_auth_token():
        app_name = config.APP_NAME
        client_id = config.CLIENT_ID
        client_secret = config.CLIENT_SECRET

        # Raise an error if any required variable is missing
        missing_keys = []
        if not app_name:
            missing_keys.append("AZAMPAY_APP_NAME")
        if not client_id:
            missing_keys.append("AZAMPAY_CLIENT_ID")
        if not client_secret:
            missing_keys.append("AZAMPAY_CLIENT_SECRET")

        if missing_keys:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_keys)} in .env file")

        url = f"{AzamPay.get_env_urls()['auth_url']}/AppRegistration/GenerateToken"
        headers = {"Content-Type": "application/json"}
        payload = {
            "appName": app_name,
            "clientId": client_id,
            "clientSecret": client_secret
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("data", {}).get("accessToken")
        else:
            raise AuthenticationError(f"Auth failed: {response.status_code} - {response.text}")

    @staticmethod
    def mno_checkout(mobile_number, amount, currency, provider, external_id):
        token = AzamPay.get_auth_token()
        url = f"{AzamPay.get_env_urls()['checkout_url']}/azampay/mno/checkout"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "accountNumber": mobile_number,
            "additionalProperties": {
                "property1": 878346737777,
                "property2": 878346737777
            },
            "amount": str(amount),
            "currency": currency,
            "externalId": external_id,
            "provider": provider
        }

        response = requests.post(url, json=payload, headers=headers)
        return response.json(), external_id
