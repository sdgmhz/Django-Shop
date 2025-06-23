import requests
import json

class IranKishSandbox:
    _payment_request_url = "https://sandbox.ipay.ir/api/v1/payment"
    _payment_verify_url = "https://sandbox.ipay.ir/api/v1/payment/verify"
    _callback_url = "http://redreseller.com/verify"

    def __init__(self, api_key):
        self.api_key = api_key
        self._headers = {
            "Content-Type": "application/json",
            "Api-Key": self.api_key
        }

    def payment_request(self, amount, order_id="order-1234", description="پرداخت کاربر"):
        payload = {
            "amount": int(amount),
            "order_id": order_id,
            "callback_url": self._callback_url,
            "description": description
        }
        response = requests.post(self._payment_request_url, json=payload, headers=self._headers)
        try:
            data = response.json()
        except Exception:
            print("Failed to parse JSON. Raw response:")
            print(response.text)
            raise
        return data

    def payment_verify(self, transaction_id):
        payload = {"transaction_id": transaction_id}
        response = requests.post(self._payment_verify_url, json=payload, headers=self._headers)
        try:
            data = response.json()
        except Exception:
            print("Failed to parse JSON. Raw response:")
            print(response.text)
            raise
        return data

    def generate_payment_url(self, token):
        return f"https://sandbox.ipay.ir/payment/{token}"

if __name__ == "__main__":
    ipay = IranKishSandbox(api_key="demo_api_key")

    resp = ipay.payment_request(20000)
    print("Payment request response:", resp)

    input("Press enter to generate payment url...")
    if "token" in resp:
        print("Payment URL:", ipay.generate_payment_url(resp["token"]))
    else:
        print("Payment request failed!")

    input("Press enter to verify payment...")
    if "transaction_id" in resp:
        verify_resp = ipay.payment_verify(resp["transaction_id"])
        print("Verification response:", verify_resp)
    else:
        print("No transaction id to verify.")
