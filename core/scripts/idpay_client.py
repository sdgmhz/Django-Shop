import requests
import json



class IDPaySandbox:
    _payment_request_url = "https://api.idpay.ir/v1.1/payment"
    _payment_verify_url = "https://api.idpay.ir/v1.1/payment/verify"
    _callback_url = "http://redreseller.com/verify"

    def __init__(self, api_key):
        self.api_key = api_key
        self._headers = {
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key,
            "X-SANDBOX": "1"
        }

    def payment_request(self, amount, description="پرداختی کاربر", order_id="order-1234"):
        payload = {
            "order_id": order_id, # may obtain from OrderModel (id)
            "amount": int(amount),
            "callback": self._callback_url,
            
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

    def payment_verify(self, id_, order_id):
        payload = {
            "id": id_,
            "order_id": order_id
        }

        response = requests.post(self._payment_verify_url, json=payload, headers=self._headers)
        
        try:
            data = response.json()
        except Exception:
            print("Failed to parse JSON. Raw response:")
            print(response.text)
            raise

        return data

    def generate_payment_url(self, link):
        return link


if __name__ == "__main__":
    idpay = IDPaySandbox(api_key="demo_api_key")

    response = idpay.payment_request(15000)
    print(response)

    input("process to generating payment url?")
    print(idpay.generate_payment_url(response["link"]))

    input("check the payment?")
    response = idpay.payment_verify(response["id"], "order-1234")
    print(response)
