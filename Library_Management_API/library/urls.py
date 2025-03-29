from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('books', views.BooksViewSet, basename='books')
router.register('transactions', views.TransactionViewSet,
                basename='transactions')


urlpatterns = [
    path('', include(router.urls))
]
