from django.urls import path,include
from .views import RegisterView,LogoutView,LoginView,PasswordResetConfirmView,RequstPasswordResetEmail

urlpatterns=[
                path("signup/", RegisterView.as_view(), name="signup"),
                path("logout/", LogoutView.as_view(), name="logout"),
                path('login/', LoginView.as_view(), name='login'),
                path('reset-password/', RequstPasswordResetEmail.as_view(), name='reset-password'),
                path('reset-password-confirm/<str:public_id>/<str:token>/', PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
]
