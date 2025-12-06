import requests
import csv
import time

API_KEY = "your_api_key"
QUERY = "Mark Carney"
OUTPUT = "nyt_carney_p1_to_p5.csv"

START_PAGE = 1
END_PAGE = 5        # inclusive
SLEEP_SECONDS = 0.3


def fetch_page(page):
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    params = {
        "q": QUERY,
        "api-key": API_KEY,
        "page": page,
        "sort": "relevance",
    }

    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()

    return data["response"]["docs"], data["response"].get("meta", {})


def main():
    rows = []
    seen_urls = set()

    for page in range(START_PAGE, END_PAGE + 1):
        print(f"Fetching page={page} ...")

        try:
            docs, meta = fetch_page(page)
        except requests.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            break

        if not docs:
            print(f"No docs on page {page}, stopping early.")
            break

        # Add docs without duplicates
        for d in docs:
            url = d.get("web_url", "")

            if url in seen_urls:
                continue
            seen_urls.add(url)

            rows.append({
                "headline": d.get("headline", {}).get("main", ""),
                "pub_date": d.get("pub_date", ""),
                "abstract": d.get("abstract", ""),
                "snippet": d.get("snippet", ""),
                "url": url,
                "source": d.get("source", ""),
            })

        time.sleep(SLEEP_SECONDS)

    if not rows:
        print("No rows fetched — nothing to save.")
        return

    # Write CSV
    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {len(rows)} unique NYT articles to {OUTPUT}")


if __name__ == "__main__":
    main()
