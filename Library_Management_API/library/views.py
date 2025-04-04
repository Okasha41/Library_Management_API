from rest_framework import status, filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import BooksSerializer, TransactionCheckOutSerializer, TransactionReturnSerializer, RegisterSerializer, TransactionSerializer
from .models import Book, Transaction


class RegisterView(APIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "This endpoint supports POST requests for user registration."})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)

        except TokenError:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BooksViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer

    # Add ordering and search filters
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    filterset_fields = ['balance']  # Direct filtering by field value
    ordering_fields = ['title', 'author', 'balance', 'total_copies']
    search_fields = ['title', 'author', 'isbn']

    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        queryset = Book.objects.filter(balance__gt=0)  # Only available books

        # Retrieve query params
        title = self.request.query_params.get('title')
        author = self.request.query_params.get('author')
        isbn = self.request.query_params.get('isbn')

        # Apply filters if they are provided
        if title:
            queryset = queryset.filter(title__icontains=title)

        if author:
            queryset = queryset.filter(author__icontains=author)

        if isbn:
            queryset = queryset.filter(isbn=isbn)

        return queryset


class TransactionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'checkout_book':
            return TransactionCheckOutSerializer
        elif self.action == 'return_book':
            return TransactionReturnSerializer
        else:
            return TransactionSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def checkout_book(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Book checked out successfully'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def return_book(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Book returned successfully'}, status=status.HTTP_200_OK)
