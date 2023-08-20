import requests
import pandas as pd
from selectolax.parser import HTMLParser


def fetch_organic_results(query, start=0):
    """Fetch organic search results from Google for a given query and page start index.

    Args:
        query (str): The search query.
        start (int, optional): The page's start index. Defaults to 0.

    Returns:
        bytes: Raw HTML content of the search results page.
    """

    # User-Agent header to emulate a real browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Construct the Google search URL
    url = f"https://www.google.com/search?q={query}&start={start}"

    # Send GET request and return the page content
    response = requests.get(url, headers=headers)
    return response.content


def parse_organic_results(html_content):
    """Parse raw HTML content of a organic search results page from Google.

    Args:
        html_content (bytes): Raw HTML content of the search results page.

    Returns:
        list[dict]: List of dictionaries containing the title, URL, and meta description of each result.
    """

    # Parse the HTML content using selectolax
    tree = HTMLParser(html_content)
    results = []

    # Loop through each search result
    for result in tree.css('div.tF2Cxc'):
        # Extract the title, if available
        title_node = result.css_first('h3')
        title = title_node.text() if title_node else None

        # Extract the URL, if available
        url_node = result.css_first('a')
        url = url_node.attributes.get('href') if url_node else None

        # Extract the meta description, if available
        meta_node = result.css_first("div[class*='VwiC3b'] span:nth-child(2)")
        if not meta_node:
            meta_node = result.css_first("div[class*='VwiC3b'] span")

        meta = meta_node.text() if meta_node else None

        # Append the extracted data to the results list
        results.append({'Title': title, 'URL': url, 'Meta Description': meta})

    return results


if __name__ == "__main__":
    # Define the search query
    query = "web scraping tools"
    all_results = []

    # Fetch and parse results from the first 3 pages
    for page in range(3):
        print(f"Fetching results from page {page + 1}...")

        # Fetch raw HTML content
        html_content = fetch_organic_results(query, start=page * 10)

        # Parse the fetched content and extend the all_results list
        all_results.extend(parse_organic_results(html_content))

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(all_results)

    # Format the filename using the query term and save the DataFrame to a CSV file
    filename = f"{query.replace(' ', '_')}_organic_results.csv"
    df.to_csv(filename, index=False)

    # Print the completion message
    print(f"Results saved to {filename}!")
