from .views import *
from django.urls import path

urlpatterns = [
    path('company-register/', CompanyRegisterView.as_view(), name='company-register'),
    path('company-login/', CompanyLoginView.as_view(), name='company-login'),

    path('user-register/', UserRegisterView.as_view(), name='user-register'),
    path('user-login/', UserLoginView.as_view(), name='user-login'),

    path('employee-login/', EmployeeLoginView.as_view(), name='employee-login'),

    path('logout/', LogoutView.as_view(), name='employee-logout'),
    path('refresh-token/', CustomTokenRefreshView.as_view(), name='token_refresh'),

    path('company-profile/', UserProfileListAPIView.as_view(), name='user-list'),
    path('user-profile/', UserListAPIView.as_view(), name='user-list'),
    # path('user/<int:pk>/', UserProfileRetrieveUpdateAPIView.as_view(), name='user-detail'),

    path('openings/', OpeningsListAPIView.as_view(), name='openings-list'),
    path('openings_two/', OpeningsTwoListAPIView.as_view(), name='openings_two-list'),
    path('openings_three/', OpeningsSreeListAPIView.as_view(), name='openings_three-list'),


]