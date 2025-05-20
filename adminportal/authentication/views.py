from django.shortcuts import render

# Create your views here.
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny

class AdminTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)