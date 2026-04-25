import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

GOODREADS_API_KEY = os.getenv('GOODREADS_API_KEY')

url = "https://goodreads12.p.rapidapi.com/searchBooks"

querystring = {"keyword":"the city and its uncertain walls","page":"1"}

headers = {
	"x-rapidapi-key": GOODREADS_API_KEY,
	"x-rapidapi-host": "goodreads12.p.rapidapi.com",
	"Content-Type": "application/json"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

books = response.json()

first_book = books[0]

print("Title of the first book:", first_book['title'])

# print(response.json())