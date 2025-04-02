from rest_framework import status, generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from .serializers import BooksSerializer, TransactionCheckOutSerializer, TransactionReturnSerializer, UserRegisterSerializer, TransactionSerializer
from .models import Book, CustomUser, Transaction


class UserViewSet(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer


class BooksViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAdminUser()]


class TransactionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'checkout_book':
            return TransactionCheckOutSerializer
        elif self.action == 'return_book':
            return TransactionCheckOutSerializer
        else:
            return TransactionSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def checkout_book(self, request):
        serializer = TransactionCheckOutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def return_book(self, request):
        serializer = TransactionReturnSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
