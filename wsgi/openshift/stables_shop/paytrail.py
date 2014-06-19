__author__ = 'jorutila'
import requests
import json
import hashlib

MERCHANT_ID="13466"
MERCHANT_PASS="6pKF4jkv97zmqBJ3ZL8gUw5DfT2NMQ"
SERVICE_URL="https://payment.paytrail.com/api-payment/create"
AUTH_HELP=(MERCHANT_ID, MERCHANT_PASS)
headers = {'content-type': 'application/json', 'X-Verkkomaksut-Api-Version': '1'}

def createPayment(order, amount, transaction_id, urls):
    data = {
        "orderNumber": transaction_id,
        "currency": "EUR",
        "locale": "fi_FI",
        "urlSet": urls,
        "orderDetails": {
            "includeVat": "1",
            "contact": {
                "telephone": "041234567",
                "mobile": "041234567",
                "email": "tester@esimerkkikauppa.fi",
                "firstName": "Simon",
                "lastName": "Seller",
                "companyName": "",
                "address": {
                    "street": "Test street 1",
                    "postalCode": "12340",
                    "postalOffice": "Helsinki",
                    "country": "FI"
                }
            },
            "products": [
                {
                    "title": "10ratsastuskortti",
                    "code": "3",
                    "amount": "1.00",
                    "price": "100.00",
                    "vat": "10.00",
                    "discount": "0.00",
                    "type": "1"
                }
            ]
        }
    }
    r = requests.post(SERVICE_URL,headers=headers, auth=AUTH_HELP, data=json.dumps(data))
    r.raise_for_status()
    return r.json()['url']

def calcAuthCode(order_number, timestamp, paid, method):
    auth = order_number+"|"+timestamp+"|"+paid+"|"+method+"|"+MERCHANT_PASS
    return hashlib.md5(auth).hexdigest()

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        print "authcode"
        params = sys.argv[1].split("&")
        aa = {}
        for p in params:
            p = p.split("=")
            aa[p[0].lower()] = p[1]
        del aa["return_authcode"]
        print calcAuthCode(**aa)
    else:
        print "Makin payment"
        print createPayment()
