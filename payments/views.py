import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .credentials import consumer_key, consumer_secret, business_short_code, passkey
import base64

def get_access_token():
    url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(url, auth=(consumer_key, consumer_secret))
    return response.json().get('access_token')

def generate_password():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password_str = business_short_code + passkey + timestamp
    encoded_password = base64.b64encode(password_str.encode()).decode('utf-8')
    return encoded_password, timestamp

def stk_push(request):
    access_token = get_access_token()
    password, timestamp = generate_password()

    url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers = {'Authorization': f'Bearer {access_token}'}

    payload = {
        "BusinessShortCode": 174379,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254798597372,
        "PartyB": 174379,
        "PhoneNumber": 254798597372,
        "CallBackURL": "https://mpesadaraja.azurewebsites.net/",
        "AccountReference": "Test123",
        "TransactionDesc": "Payment for X service"
    }

    response = requests.post(url, json=payload, headers=headers)
    return JsonResponse(response.json())

@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        print(f"Callback Data: {data}")
        return JsonResponse({"Result": "Received"})
