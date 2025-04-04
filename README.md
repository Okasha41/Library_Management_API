# Library_Management_API

ALX Capstone Project - Library Management System

------------------------- User Management Endpoints -----------------------------
#################################################################################

1- Register new user [Permission : Anyone is allowed]

url : POST /library/users/register/

request body :
{
"username" : "test",
"email" : "test@me.com",
"password" : "123456789",
"first_name" : "a",
"last_name" : "b"
}

Response if username or email already exsits:
{
"username": [
"A user with that username already exists."
],
"email": [
"user with this email already exists."
]
}

Response if data is valid:
{
"message": "User registered successfully."
}

---

2- Login with user credentials [Permission : Anyone is allowed]

url : POST /library/users/login/

request body :
{
"username": "okasha",
"password": "123456789"
}

response if login is successful:
{
"refresh": "...",
"access": "..."
}

response if login failed:
{
"detail": "No active account found with the given credentials"
}

---

3- Refresh access token if it expired [Permission : Anyone is allowed]

"lifetime for access token is 1 hour and for refresh token is 7 day"

url : POST /library/users/refresh/

request body:
{
"refresh": "..."
}

response if the given refresh token is valid:
{
"access": "...",
"refresh": "..."
}

response if the given refresh token in not valid:
{
"detail": "Token is invalid",
"code": "token_not_valid"
}

---

4- Logout [Permission : Only Authenticated]

url : POST /library/users/logout/

Bearer Token : "... "
request body:
{
"refresh": "..."
}

response:
{
"message": "Successfully logged out."
}

------------------------- Book Management Endpoints -----------------------------
#################################################################################

1- List available books [Permission : Anyone is allowed]

url : GET /library/books/

response :
{
"total_count": 3,
"total_pages": 1,
"current_page": 1,
"next": null,
"previous": null,
"results": [...]
}

2- Add new book to library [Permission : Admin only]

url : POST /library/books/

Beaer Token : "..."
request body:
{
"title": "Python",
"author": "Okasha1",
"isbn": "1234567891337",
"published_date": "2020-12-01",
"total_copies": 3,
"balance": 3
}

response if book with same isbn exists:
{
"isbn": [
"book with this isbn already exists."
]
}

response in case add book successfully:
{
"id": 5,
"title": "Python",
"author": "Okasha1",
"isbn": "1234567892337",
"published_date": "2020-12-01",
"total_copies": 3,
"balance": 3
}

3- Update/Detete a book from library [Permission : Admin only]
url : PATCH/DELETE /library/books/<int:book_id>

Beaer Token : "..."
request body:
{
"title": "Python",
"author": "Okasha1",
"isbn": "1234567891337",
"published_date": "2020-12-01",
"total_copies": 3,
"balance": 3
}

response if update is successful:
{
"title": "Python",
"author": "Okasha1",
"isbn": "1234567891337",
"published_date": "2020-12-01",
"total_copies": 3,
"balance": 3
}

---------------------- Transactions Management Endpoints ------------------------
#################################################################################

1- List all transactions of current logged in user

url : POST /library/transactions/

Bearer token: "..."

response:
{
"total_count": 1,
"total_pages": 1,
"current_page": 1,
"next": null,
"previous": null,
"results": [
{
"id": 4,
"book": 2,
"user": 3,
"transaction_date": "2025-04-03T03:34:04.389813Z",
"due_date": "2025-04-17T03:34:04.389220Z",
"return_date": null,
"status": "checked_out"
}
]
}

2- Check out a book [Permission : Authenticated only]

url : POST /library/transactions/checkout_book/

Bearer token: "..."
request body:
{
"book": 2
"due_date": 2025-04-20 # if not provided will be considered after 14 days of check out date
}

response in case check out is successfull:
