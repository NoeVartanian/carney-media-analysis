"""
This script fetches news articles regarding Mark Carney from the News API and saves them to a JSON file.

Updated: 
    - Added an extra argument to specify the number of articles to fetch.
    - Added a parameter to the API request to filter out articles published before a given date.

Arguments:
    outlet: The outlet to fetch news from
    api_token: The API token
    -o, --output: The output file name
    -n, --number: The number of articles to fetch

Returns:
    A JSON file containing the raw API responses

Usage: 
    python get_news_from_API.py <outlet> <api_token> [-o <output>] [-n <number>]

Example:
    python get_news_from_API.py 'cbc.ca' 'your_api_token' -o 'cbc.json' -n 100
"""


import argparse
import json
import random
import requests
import time


def getNews(outlet, search, api_token, url, number_of_articles):
    """
    Fetches news articles from the News API and saves them to a JSON file.
    """
    # Initialize raw responses list
    raw_responses = []
    
    # Fetch news articles
    number_of_pages = (number_of_articles - 1) // 3 + 1     # 3 articles per page due to API limit
    for i in range(number_of_pages):  
        parameters = {
            "api_token": api_token,
            "search": search,
            "language": "en",
            "domains": outlet,
            "limit": 3,         # limit to 3 articles per page
            "page": i + 1,      # IMPORTANT: paginate to avoid duplicates
            "published_after": "2024-09-01"         # We only fetch articles after Sept. 1, 2024 =============== EDIT?
        }

        response = requests.get(url, params=parameters)

        data = response.json()

        # If no articles were returned, stop retrieving pages.
        if data["meta"]["returned"] == 0:
            print(f'No articles found at page {i+1}.')
            print("Exiting.")
            break

        raw_responses.append(data)
        print(f"Fetched {i+1} pages.")

        time.sleep(random.uniform(0.2, 0.5))  # avoid rate limiting
    return raw_responses


def main():
    parser = argparse.ArgumentParser(description="Fetch news articles by the news api")
    parser.add_argument('outlet', type=str, help="The outlet to fetch news from")
    parser.add_argument('api_token', type=str, help="The API token")
    parser.add_argument('-o','--output', type=str, default="news.json", help="The output file name")
    parser.add_argument('-n','--number', type=int, default=100, help="The number of articles to fetch")
    args = parser.parse_args()

    # News API
    # Fixed parameters
    url = "https://api.thenewsapi.com/v1/news/all"
    search = "Mark Carney"

    raw_responses = getNews(args.outlet, search, args.api_token, url, args.number)

    # Save all raw API responses into one json file
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(raw_responses, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
    
