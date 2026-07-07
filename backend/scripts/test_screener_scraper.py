import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
}

all_rows = []

for page in range(1, 4):

    url = (
        "https://www.screener.in/"
        "screen/raw/"
        "?sort=&order=&source_id="
        "&query=Market+Capitalization+%3E+0"
        f"&page={page}"
    )

    print("\n" + "=" * 70)
    print(f"Fetching page {page}")
    print("=" * 70)

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    print("Status:", response.status_code)
    print("Final URL:", response.url)

    print("\nFIRST 1000 CHARACTERS OF RESPONSE:\n")
    print(response.text[:1000])

    print("\n" + "=" * 70)

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    table = soup.find("table")

    if table is None:
        print("No table found")
    else:
        print("TABLE FOUND!")

        rows = table.find_all("tr")
        print("Rows:", len(rows))

        for row in rows:
            cols = row.find_all(["td", "th"])

            values = [
                c.get_text(strip=True)
                for c in cols
            ]

            if len(values) > 0:
                all_rows.append(values)

    time.sleep(
        random.uniform(2, 5)
    )

print("\nTOTAL ROWS:", len(all_rows))

df = pd.DataFrame(all_rows)

df.to_csv(
    "test_screener.csv",
    index=False
)

print("\nSaved test_screener.csv")