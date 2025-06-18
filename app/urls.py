from django.urls import path
from django.views.generic import TemplateView
# from rest_framework import router
from .views import RegisterView, LoginView, UserList, ChatDash
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-list/', UserList.as_view(), name='user-list'),

    path('register-page/', TemplateView.as_view(template_name='app/register.html'), name='register-page'),
    path('login-page/', TemplateView.as_view(template_name='app/login.html'), name='login-page'),
    path('chat-page/', TemplateView.as_view(template_name='app/chatdash.html'), name='chat-page'),
    path('chat-page/<int:id>/<str:name>/', ChatDash, name='chat-page-specific'),
]
