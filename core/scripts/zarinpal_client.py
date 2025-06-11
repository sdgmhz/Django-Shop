import requests


class ZarinPalSandbox:
    _payment_request_url = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    _payment_verify_url = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
    _payment_page_url = "https://sandbox.zarinpal.com/pg/StartPay/"
    _callback_url = "127.0.0.1:8000/"

    def __init__(self, merchant_id):
        self.merchant_id = merchant_id

    def payment_request(self,amount, description="پرداختی کاربر"):
        payload = {
                    "merchant_id": self.merchant_id,
                    "amount": int(amount),
                    "callback_url": self._callback_url,
                    "description": description
        }
    

        response = requests.post(self._payment_request_url, json=payload)


        return response.json()


    def payment_verify(self, amount, authority):
        payload = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "authority": authority
        }
       
        response = requests.post(self._payment_verify_url, json=payload)

        return response.json()

    def generate_payment_url(self,authority):
        return self._payment_page_url + authority
    

if __name__ == "__main__":
    zarinpal = ZarinPalSandbox(merchant_id="927d65e3-923b-4efa-9922-1fff10f166e3")
    response = zarinpal.payment_request(15000)
    print(response)

    input("process to generating payment url?")
    print(zarinpal.generate_payment_url(response["data"]["authority"]))

    input("check the payment?")
    response = zarinpal.payment_verify(15000, response["data"]["authority"])
    print(response)