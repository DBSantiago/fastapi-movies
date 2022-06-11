import requests

URL_REVIEWS = "http://localhost:8000/api/v1/reviews"
HEADERS = {
    "accept": "application/json"
}
QUERY_SET = {
    "page": 1,
    "limit": 2
}

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
