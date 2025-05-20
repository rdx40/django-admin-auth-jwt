from django.urls import path
from .views import AdminTokenObtainPairView

urlpatterns = [
    path('login/', AdminTokenObtainPairView.as_view(), name='token_obtain_pair'),
]