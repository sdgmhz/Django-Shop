import requests

class NextPaySandbox:
    _token_url = "https://app-sandbox.nextpay.world/nx/gateway/token"
    _verify_url = "https://app-sandbox.nextpay.world/nx/gateway/verify"
    _callback_url = "http://redreseller.com/verify"

    def __init__(self, api_key):
        self.api_key = api_key

    def payment_request(self, amount, order_id="order-1234", description="درخواست پرداخت"):
        payload = {
            "api_key": self.api_key,
            "amount": int(amount),
            "order_id": order_id,
            "callback_uri": self._callback_url,
            "description": description
        }
        response = requests.post(self._token_url, json=payload)
        data = response.json()
        return data

    def generate_payment_url(self, token):
        return f"https://nextpay.org/nx/gateway/{token}"

    def payment_verify(self, token):
        payload = {
            "api_key": self.api_key,
            "token": token
        }
        resp = requests.post(self._verify_url, json=payload)
        return resp.json()

if __name__ == "__main__":
    np = NextPaySandbox(api_key="ck_sandbox_w8a0pxa2y260nz01dl6npxof")
    response = np.payment_request(10000)
    print("Token response:", response)

    token = response.get("token")
    print("Go pay at:", np.generate_payment_url(token))

    input("check payment?")
    result = np.payment_verify(token)
    print("Verification result:", result)
