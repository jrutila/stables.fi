__author__ = 'jorutila'
import requests
import json
import hashlib
from django.conf import settings
from decimal import Decimal

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
        "price": str(order.order_total)
    }
    """
    VAT = getattr(settings, 'SHOP_VAT', Decimal('0.24'))
    for o in order.items.all():
        data['orderDetails']['products'].append(
            {
                "title": o.product_name,
                "code": str(o.product.id),
                "amount": str(o.quantity),
                "price": str((o.line_total*(1+VAT)).quantize(Decimal('0.01'))),
                "vat": str(VAT*100),
                "discount": "0.00",
                "type": "1"
            }
        )
    """
    r = requests.post(SERVICE_URL, headers=headers, auth=AUTH_HELP, data=json.dumps(data))
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
