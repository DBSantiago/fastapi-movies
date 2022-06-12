import requests

URL_REVIEWS = "http://localhost:8000/api/v1/reviews"
HEADERS = {
    "accept": "application/json"
}
QUERY_SET = {
    "page": 1,
    "limit": 2
}
REVIEW = {
    "user_id": 7,
    "movie_id": 1,
    "review_text": "It left me speechless",
    "score": 5
}

# ======================================
#             POST REQUEST
# ======================================

# response = requests.post(URL_REVIEWS, json=REVIEW)
#
# if response.status_code == 200:
#     print(f"Review created successfully")

# ======================================
#             GET REQUEST
# ======================================

# response = requests.get(URL_REVIEWS, headers=HEADERS, params=QUERY_SET)
#
# if response.status_code == 200:
#     print("Request successful")
#     print(response.content)
#     print(response.headers)
#
#     if response.headers.get("content-type") == "application/json":
#         print(response.json())
#
#         reviews = response.json()
#
#         for review in reviews:
#             print(f"Movie: {review['movie']['title']} - Score: {review['score']}")

# ======================================
#             PUT REQUEST
# ======================================

# REVIEW_ID = 10
# UPDATED_REVIEW = {
#     "review_text": "It was pretty good",
#     "score": 4
# }
# response = requests.put(URL_REVIEWS + f"/{REVIEW_ID}", json=UPDATED_REVIEW)
#
# if response.status_code == 200:
#     print("PUT Request successful")
#     print(response.json())

# ======================================
#             DELETE REQUEST
# ======================================

# response = requests.delete(URL_REVIEWS + f"/{REVIEW_ID}")
#
# if response.status_code == 200:
#     print("DELETE Request successful")
#     print(response.json())

# ======================================
#        POST REQUEST - COOKIES
# ======================================
URL_LOGIN = "http://localhost:8000/api/v1/users/login"
URL_USER_REVIEWS = "http://localhost:8000/api/v1/users/reviews"
USER = {
    "username": "username",
    "password": "password"
}
response = requests.post(URL_LOGIN, json=USER)

if response.status_code == 200:
    print("User authenticated successfully")

    print(response.json())

    user_id = response.cookies.get_dict().get("user_id")
    print(user_id)

    cookies = {
        "user_id": user_id
    }

    response = requests.get(URL_USER_REVIEWS, cookies=cookies)

    if response.status_code == 200:
        for review in response.json():
            print(f"Movie: {review['movie']['title']} - Score: {review['score']}")
