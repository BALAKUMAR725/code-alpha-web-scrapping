import requests
from bs4 import BeautifulSoup
import pandas as pd

# IMDb Top 250 URL
url = "https://www.imdb.com/chart/top/"

# Headers to mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Send request
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# List to store movie data
all_movies = []

# Locate each row of the movie list
rows = soup.select("li.ipc-metadata-list-summary-item")

for row in rows:
    try:
        # Extract title
        title_tag = row.select_one("h3")
        title = title_tag.text.strip() if title_tag else "N/A"

        # Extract year (inside <span>)
        year_tag = row.find("span", class_="sc-14dd939d-6")
        year = year_tag.text.strip("()") if year_tag else "N/A"

        # Extract rating (inside <span> with star icon)
        rating_tag = row.find("span", class_="ipc-rating-star")
        rating = rating_tag.text.strip() if rating_tag else "N/A"

        # Save to list
        all_movies.append({
            "Title": title,
            "Year": year,
            "Rating": rating
        })

    except Exception as e:
        continue

# Create DataFrame
df = pd.DataFrame(all_movies)

# Show sample data
print("\nSample data:")
print(df.head())

# Save to CSV
df.to_csv("CodeAlpha_WebScraping_IMDb_Top250.csv", index=False)
print("\nScraping complete! Data saved to 'CodeAlpha_WebScraping_IMDb_Top250.csv'")
