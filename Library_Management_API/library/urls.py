from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views


router = DefaultRouter()
router.register('books', views.BooksViewSet, basename='books')
router.register('transactions', views.TransactionViewSet,
                basename='transactions')


urlpatterns = [
    path('', include(router.urls)),
    path('users/login/', TokenObtainPairView.as_view(), name='login'),
    path('users/register/', views.RegisterView.as_view(), name='register'),
    path('users/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('users/logout/', views.LogoutView.as_view(), name='logout'),
]
