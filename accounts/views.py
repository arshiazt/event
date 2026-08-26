from django.contrib.auth import login,logout
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.serializers import RegisterSerializer,LoginSerializer
from accounts.permissions import IsNotAuthenticated

# Create your views here.

class RegisterView(APIView):
    permission_classes = [IsNotAuthenticated]

    def post(self,request):

        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request,user)

        return Response({
            'message':'Registration was successful',
            'phone':user.phone,
            'role':'organizer' if user.organizer else 'participant',
        },
        status =  status.HTTP_201_CREATED
        )

class LoginView(APIView):
    permission_classes = [IsNotAuthenticated]

    def post(self,request):

        serializer = LoginSerializer(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request,user)

        return Response({
            "detail": "Login successful",
            "role": "organizer" if user.organizer else "participant"
        },
        status=status.HTTP_200_OK
        )