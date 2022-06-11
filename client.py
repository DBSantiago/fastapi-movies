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
response = requests.post(URL_REVIEWS, json=REVIEW)

if response.status_code == 200:
    print(f"Review created successfully")

response = requests.get(URL_REVIEWS, headers=HEADERS, params=QUERY_SET)

if response.status_code == 200:
    print("Request successful")
    print(response.content)
    print(response.headers)

    if response.headers.get("content-type") == "application/json":
        print(response.json())

        reviews = response.json()

        for review in reviews:
            print(f"Movie: {review['movie']['title']} - Score: {review['score']}")

REVIEW_ID = 10
UPDATED_REVIEW = {
    "review_text": "It was pretty good",
    "score": 4
}
response = requests.put(URL_REVIEWS + f"/{REVIEW_ID}", json=UPDATED_REVIEW)

if response.status_code == 200:
    print("PUT Request successful")
    print(response.json())

response = requests.delete(URL_REVIEWS + f"/{REVIEW_ID}")

if response.status_code == 200:
    print("DELETE Request successful")
    print(response.json())
