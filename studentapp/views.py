from rest_framework.decorators import api_view
from .serializer import UserSerializer
from rest_framework.response import Response
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
# Create your views here.

@api_view(['POST'])
def registerview(request):
    serializer=UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"message":"Sucessfully Registered!!!"})


@api_view(['POST'])
def loginview(request):
    
    email=request.data['email']
    password=request.data['password']

    user=User.objects.filter(email=email).first()

    if user is None:
        raise AuthenticationFailed('User Not Found!!!')

    if not user.check_password(password):
        raise AuthenticationFailed('Incorrect Password!!')
    
    accesstokenexpiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
    payload = {
        'id': user.id,
        'exp': accesstokenexpiry,
        'iat': datetime.datetime.utcnow()
    }
    accesstoken=jwt.encode(payload,'secret',algorithm='HS256')

    refreshtokenexpiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=3)
    refreshpayload = {
        'id': user.id,
        'exp': refreshtokenexpiry,
        'iat': datetime.datetime.utcnow()
    }
    refreshtoken = jwt.encode(refreshpayload, 'secret', algorithm='HS256') 


    response=Response()
    response.set_cookie( key='accessToken',value=accesstoken,httponly=True,expires=accesstokenexpiry)
    response.set_cookie( key='refershToken',value=refreshtoken,httponly=True,expires=refreshtokenexpiry)

    response.data={"accessToken":accesstoken,"refreshToken":refreshtoken}
    return response


@api_view(['GET'])
def userview(request):
    accessToken = request.COOKIES.get('accessToken')
    refreshToken = request.COOKIES.get('refershToken')
    response = Response()  
    
    
    if not accessToken:
        if not refreshToken:
            raise AuthenticationFailed("Unauthenticated!!!")
        else:
            try:
                payloadRefreshToken = jwt.decode(refreshToken, 'secret', algorithms=['HS256'])
                
                accesstokenexpiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
                payload = {
                    'id': payloadRefreshToken['id'],
                    'exp': accesstokenexpiry,
                    'iat': datetime.datetime.utcnow()
                }
                accessToken = jwt.encode(payload, 'secret', algorithm='HS256')
                
                response.set_cookie(key='accessToken', value=accessToken, httponly=True, expires=accesstokenexpiry)

            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed("Invalid Token!! Please Re-login...!")

  
    try:
        payload = jwt.decode(accessToken, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Access token expired. Please Re-login...!")
    
    
    user = User.objects.filter(id=payload['id']).first()

    if not user:
        raise AuthenticationFailed("User not found!")
    
    serializer = UserSerializer(user)

   
    response.data = serializer.data

    return response


@api_view(['POST'])
def logoutview(request):
    response = Response()
   
    response.delete_cookie('accessToken')
    response.delete_cookie('refreshToken')

    response.data = {"message": "Logged out successfully"}

    return response