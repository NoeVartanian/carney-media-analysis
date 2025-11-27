"""
This file is used to extract news articles from a JSON file and save to a CSV file.


Updated: 
    - Added Description and Keywords columns
    - Removed the irrelevant messages (such as "Read more" or advertisements) in snippet columns only

Arguments:
    input: The input JSON file
    output: The output CSV file

Returns:
    A CSV file containing the extracted news articles, with the following columns:
    - ArticleID: The ID of the article
    - url: The URL of the article
    - Source: The source outlet of the article
    - Headline: The title of the article
    - Date: The date of the article
    - Snippet: The snippet of the article
    - Description: The description of the article (Updated)
    - Keywords: The keywords of the article (Updated)

Usage: 
    python extract_to_csv.py -i <input> -o <output>

Example:
    python extract_to_csv.py -i 'cbc.json' -o 'cbc.csv'
"""

import argparse
import csv
import datetime
import json

def write_csv(args, raw_responses,row_names):
    data_list = []

    with open(args.output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(row_names)
    
        for page_data in raw_responses:
            articles = page_data['data']
            for article in articles:
                ArticleID = article['uuid']
                url = article['url']
                source = article['source']
                Headline = article['title']
                Date = datetime.datetime.fromisoformat(article['published_at']).strftime('%Y-%m-%d')
                Snippet = article['snippet'].splitlines()[-1]#get rid of the irrelevant messages
                description = article['description']
                keywords = article['keywords']
                data_list.append([ArticleID,url,source,Headline,Date,Snippet,description,keywords])
        
        writer.writerows(data_list)


def main():
    parser = argparse.ArgumentParser(description="Extract news articles from a JSON file and save to a CSV file")
    parser.add_argument('-i','--input', type=str, help="The input JSON file")
    parser.add_argument('-o','--output', type=str, help="The output CSV file")
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        raw_responses = json.load(f)

    row_names = ['ArticleID','url','Source','Headline','Date','Snippet','Description','Keywords']
    write_csv(args,raw_responses,row_names)

if __name__ == "__main__":
    main()