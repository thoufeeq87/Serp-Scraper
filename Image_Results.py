# Importing the necessary libraries:
# - `sync_playwright` allows us to work with web pages using the Playwright library in a synchronous manner.
# - `pandas` is a data manipulation library that provides structures for easily working with structured data.
from playwright.sync_api import sync_playwright
import pandas as pd

# Function to fetch image results from Google Images.
def fetch_image_results(query):
    # Using the Playwright context manager to handle the browser lifecycle.
    with sync_playwright() as p:
        # Launching a new browser instance.
        browser = p.chromium.launch()
        # Creating a new tab/page.
        page = browser.new_page()

        # Navigating to Google Images with the given search query.
        page.goto(f"https://www.google.com/search?q={query}&tbm=isch")

        # Lists to hold the fetched image URLs and their respective titles.
        image_urls = []
        image_titles = []

        # Locating all image elements on the page with the given CSS selector.
        images = page.query_selector_all("a[class='iGVLpd kGQAp BqKtob lNHeqe']")
        for img in images:
            # Extracting the href attribute, which contains the URL.
            img_url = img.get_attribute('href')
            # Extracting the title attribute, which contains the image's title/description.
            title = img.get_attribute('title')

            # Appending the fetched details to the respective lists.
            image_urls.append(img_url)
            image_titles.append(title)

        # Closing the browser after fetching the details.
        browser.close()
        # Returning the lists of image URLs and titles.
        return image_urls, image_titles

# Main execution block.
if __name__ == "__main__":
    # Specifying the search query for which we want to fetch image results.
    query = "web scraping"
    # Calling the fetch_image_results function to get image URLs and titles for the specified query.
    img_urls, img_titles = fetch_image_results(query)

    # Converting the lists of image URLs and titles into a DataFrame.
    df = pd.DataFrame({
        'Image URL': img_urls,
        'Image Title': img_titles
    })

    # Saving the DataFrame to a CSV file. The file name is based on the search query.
    file_name = f"{query}_image_results.csv"
    df.to_csv(file_name, index=False)
    # Printing out the name of the file where results have been saved.
    print(f"Saved results to {file_name}")
