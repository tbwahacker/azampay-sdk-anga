from azampay.core import AzamPay
import uuid

def main():
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

if __name__ == "__main__":
    main()
