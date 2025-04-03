from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.timezone import now, timedelta
from .models import Book, Transaction


UserModel = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email',
                  'password', 'first_name', 'last_name']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserModel.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn',
                  'published_date', 'total_copies', 'balance']
        read_only_fields = ['id']


class TransactionCheckOutSerializer(serializers.ModelSerializer):

    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Transaction
        fields = ['id', 'book', 'user',
                  'transaction_date', 'due_date', 'status']
        read_only_fields = ['id', 'user',
                            'transaction_date', 'status']

    def create(self, validated_data):
        user = self.context['request'].user
        book = validated_data.get('book')

        # check if the book is provided in validated data
        if not book:
            raise serializers.ValidationError('Book is required')

        # check if there is any overdue books for this user
        has_overdue_books = Transaction.objects.filter(
            user=user, status='overdue').exists()
        if has_overdue_books:
            raise serializers.ValidationError(
                'You have overdue books, you can not check out any books before returning the overdue books')

        # check if the user checked this book before and didn't return it yet
        if Transaction.objects.filter(user=user, book=book, status='checked_out').exists():
            raise serializers.ValidationError(
                'You have already checked out this book')

        # setting the due date after 14 days if not passed by the user
        due_date = validated_data.get('due_date', now() + timedelta(days=14))

        # checking if there are available copies for this book
        if book.balance == 0:
            raise serializers.ValidationError(
                'There are no available copies of the required book')

        transaction = Transaction.objects.create(
            user=user, book=book, status='checked_out', due_date=due_date)

        # updating number of available copies
        book.balance -= 1
        book.save()

        return transaction


class TransactionReturnSerializer(serializers.ModelSerializer):

    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Transaction
        fields = ['id', 'book', 'user',
                  'transaction_date', 'due_date', 'return_date', 'status']
        read_only_fields = ['id', 'user',
                            'transaction_date', 'status', 'return_date', 'due_date']

    def create(self, validated_data):
        user = self.context['request'].user
        book = validated_data.get('book')
        transaction = Transaction.objects.filter(
            user=user, book=book, status__in=['checked_out', 'overdue']).first()

        # check if there is a record for this book being checked out
        if not transaction:
            raise serializers.ValidationError(
                'You did not check out this book')

        # update status of tranasaction
        transaction.check_overdue()

        # check if transaction status is overdue
        if transaction.status == 'overdue':
            raise serializers.ValidationError(
                'This book is overdue and a fine must be paid')

        # updating the transaction return date and status
        transaction.return_date = now()
        transaction.status = 'returned'
        transaction.save()

        # updating quantity of available books
        book.balance += 1
        book.save()

        return transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'book', 'user',
                  'transaction_date', 'due_date', 'return_date', 'status']
