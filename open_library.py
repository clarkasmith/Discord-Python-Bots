import requests

title = "the lord of the rings"
words = title.split()
joined = "+".join(words)

url = f"https://openlibrary.org/search.json?q={joined}"
headers = {
    "User-Agent": "MyAppName/1.0 (myemail@example.com)"
}
response = requests.get(url, headers=headers)

print(response.json()["docs"][0])

