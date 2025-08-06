from azampay.core import AzamPay
import uuid
import time  # Add this import

def main():
    try:
        # Generate a unique external ID
        external_id = str(uuid.uuid4())

        # Sample mobile payment transaction details
        mobile_number = "0712345678"
        amount = 5000
        currency = "TZS"
        provider = "TIGO"  # Mpesa, Airtel, Halotel, Azampesa, Tigo

        print("Initiating MNO Checkout...")
        response, ref = AzamPay.mno_checkout(
            mobile_number=mobile_number,
            amount=amount,
            currency=currency,
            provider=provider,
            external_id=external_id
        )

        print(f"Transaction For MNO Reference: {ref}")
        print("Response:")
        print(response)

        # Delay before proceeding to bank checkout
    #     # Sample Bank payment transaction details
    #     bank_account_number = "J012323454677"
    #     mobile_number = "0712345678"
    #     merchant_name = "Anga Six"
    #     otp = ""
    #     amount = 5000
    #     currency = "TZS"
    #     provider = "CRDB"  # CRDB and NMB only supported banks
    #
    #     print("Initiating Bank Checkout...")
    #     response, ref = AzamPay.bank_checkout(
    #         bank_account_number=bank_account_number,
    #         mobile_number=mobile_number,
    #         merchant_name=merchant_name,
    #         otp=otp,
    #         amount=amount,
    #         currency=currency,
    #         provider=provider,
    #         external_id=external_id
    #     )
    #
    #     print(f"Transaction For Bank Reference: {ref}")
    #     print("Response:")
    #     print(response)
    #
    except Exception as e:
        print("Transaction failed:")
        print(str(e))

if __name__ == "__main__":
    main()
