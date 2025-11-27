"""
This script fetches news articles regarding Mark Carney from the News API and saves them to a JSON file.

Arguments:
    outlet: The outlet to fetch news from
    api_token: The API token
    -o, --output: The output file name

Returns:
    A JSON file containing the raw API responses

Usage: 
    python get_news_from_API.py <outlet> <api_token> [-o <output>]

Example:
    python get_news_from_API.py 'cbc.ca' 'your_api_token' -o 'cbc.json'
"""


import argparse
import json
import random
import requests
import time


def getNews(outlet, search, api_token,url):
    """
    Fetches news articles from the News API and saves them to a JSON file.
    """
    # Initialize raw responses list
    raw_responses = []
    
    # Fetch news articles
    for i in range(17):  # 17 requests → 51 articles
        parameters = {
            "api_token": api_token,
            "search": search,
            "language": "en",
            "domains": outlet,
            "limit": 3, # 3 articles per page due to API limit
            "page": i + 1 # IMPORTANT: paginate to avoid duplicates
        }

        response = requests.get(url, params=parameters)

        data = response.json()
        raw_responses.append(data)
        print(f"Fetched {i+1} pages.")

        time.sleep(random.uniform(0.2, 0.5))  # avoid rate limiting
    return raw_responses


def main():
    parser = argparse.ArgumentParser(description="Fetch news articles by the news api")
    parser.add_argument('outlet',type=str,help="The outlet to fetch news from")
    parser.add_argument('api_token',type=str,help="The API token")
    parser.add_argument('-o','--output',type=str,default="news.json",help="The output file name")
    args = parser.parse_args()

    # News API
    # Fixed parameters
    url = "https://api.thenewsapi.com/v1/news/all"
    search = "Mark Carney"

    raw_responses = getNews(args.outlet, search, args.api_token,url)

    # Save all raw API responses into one json file
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(raw_responses, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
    
