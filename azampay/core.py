import requests
from azampay.config import Config
from azampay.exceptions import AuthenticationError, CheckoutError, EnvironmentError, AzamPayException

config = Config()  # Create config instance


class AzamPay:
    @staticmethod
    def get_env_urls():
        try:
            if config.ENVIRONMENT == "production":
                auth_url = "https://authenticator.azampay.co.tz"
                checkout_url = "https://checkout.azampay.co.tz"
            else:
                auth_url = "https://authenticator-sandbox.azampay.co.tz"
                checkout_url = "https://sandbox.azampay.co.tz"

            return {"auth_url": auth_url, "checkout_url": checkout_url}
        except Exception as e:
            raise AzamPayException(f"Failed to determine environment URLs: {str(e)}")

    @staticmethod
    def get_auth_token():
        try:
            app_name = config.APP_NAME
            client_id = config.CLIENT_ID
            client_secret = config.CLIENT_SECRET

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

            response = requests.post(url, json=payload, headers=headers, timeout=50)
            if response.status_code == 200:
                return response.json().get("data", {}).get("accessToken")
            else:
                raise AuthenticationError(f"Auth failed: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            raise AuthenticationError(f"Auth request error: {str(e)}")
        except Exception as e:
            raise AuthenticationError(f"Unexpected error during authentication: {str(e)}")

    @staticmethod
    def mno_checkout(mobile_number, amount, currency, provider, external_id):
        try:
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

            response = requests.post(url, json=payload, headers=headers, timeout=50)
            if response.status_code in [200, 201]:
                return response.json(), external_id
            else:
                raise CheckoutError(f"Checkout failed: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            raise CheckoutError(f"Checkout request error: {str(e)}")
        except Exception as e:
            raise CheckoutError(f"Unexpected error during checkout: {str(e)}")

    @staticmethod
    def bank_checkout(bank_account_number, mobile_number, merchant_name, otp, amount, currency, provider, external_id):
        try:
            token = AzamPay.get_auth_token()
            url = f"{AzamPay.get_env_urls()['checkout_url']}/azampay/bank/checkout"
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            payload = {
                "amount": str(amount),
                "merchantAccountNumber": mobile_number,
                "merchantMobileNumber": mobile_number,
                "merchantName": merchant_name,
                "otp": otp,
                "additionalProperties": {
                    "property1": 878346737777,
                    "property2": 878346737777
                },
                "currencyCode": currency,
                "referenceId": external_id,
                "provider": provider
            }

            response = requests.post(url, json=payload, headers=headers, timeout=50)
            if response.status_code in [200, 201]:
                return response.json(), external_id
            else:
                raise CheckoutError(f"Checkout failed: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            raise CheckoutError(f"Checkout request error: {str(e)}")
        except Exception as e:
            raise CheckoutError(f"Unexpected error during checkout: {str(e)}")
