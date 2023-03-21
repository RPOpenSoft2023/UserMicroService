from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ifscApi.getDetails import FetchData
import requests
import jwt
from django.conf import settings
from django.core import exceptions

# Assign IFSC code
ifsc = 'KKBK0005652'
  
# Parse the ifsc code
data = FetchData().getdata(ifsc)
  
# Display details
print(data)

def bank_details(ifsc):
    try:
        res = requests.get("https://ifsc.razorpay.com/"+ifsc)
        return res.json()
    except Exception as e:
        return Response({'error':e},status=200)
    
def decode_token(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise Exception('Authorization header is missing')
    _, token = auth_header.split()
    try:
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return decoded_token
    except jwt.InvalidSignatureError:    
        raise Exception('Token Invalid')
    except jwt.ExpiredTokenError:
        raise Exception('Token Expired')
    except IndexError:
        raise Exception('Token prefix missing')
    except Exception as e:
        raise Exception(str(e))
    