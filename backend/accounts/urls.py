from django.urls import path
from .views import SignupView, LoginView, GoogleLoginAPIView

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path("auth/google/", GoogleLoginAPIView.as_view()),
]

