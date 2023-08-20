# Importing required libraries:
# - `pandas`: For data manipulation and to save data to CSV.
# - `sync_playwright`: For web automation to fetch dynamic content from web pages.
import pandas as pd
from playwright.sync_api import sync_playwright

# Function to extract video search results from Google for a given query.
def extract_videos(query):
    # Initializing the Playwright context.
    with sync_playwright() as p:
        # Launching a Chromium browser instance.
        browser = p.chromium.launch()
        # Opening a new page/tab.
        page = browser.new_page()

        # Directly navigating to Google's video search results for the given query.
        page.goto(f"https://www.google.com/search?q={query}&tbm=vid")
        # Waiting for the page to completely load.
        page.wait_for_load_state("networkidle")

        # List to store the extracted video data.
        video_data = []

        # Loop to traverse through search result pages: Initial page + 2 'Next' button clicks.
        for i in range(3):
            # Selecting all video elements present on the current page.
            videos = page.query_selector_all("div.v7W49e div.MjjYud")

            # Loop to process each video element.
            for vid in videos:
                # Fetching video URL and title elements.
                vid_url_element = vid.query_selector("a")
                title_element = vid.query_selector("h3")

                # If both elements are found, extract their data.
                if vid_url_element and title_element:
                    vid_url = vid_url_element.get_attribute("href")
                    title = title_element.inner_text()

                    # Filter out unwanted URLs and append data to our list.
                    if vid_url and not vid_url.startswith('/search'):
                        video_data.append([title, vid_url])

            # Navigation to the next page of search results.
            next_button = page.query_selector('a#pnnext')
            # If 'Next' button is found, click it to go to the next page.
            if next_button:
                next_button.click()
                # Wait for the new page to load.
                page.wait_for_load_state("networkidle")
            # If 'Next' button is not found, exit the loop.
            else:
                break

        # Close the browser instance after data extraction.
        browser.close()

        # Convert the list of video data to a pandas DataFrame.
        df = pd.DataFrame(video_data, columns=['Title', 'URL'])
        # Save the DataFrame to a CSV file. The filename is based on the search query.
        file_name = f"{query}_video_results.csv"
        df.to_csv(file_name, index=False)

        # Provide feedback on where the data was saved.
        print(f"\nData saved to {file_name}")

# Main execution block.
if __name__ == "__main__":
    # Specify the search query for which we want to extract video search results.
    query = "web scraping"
    # Call the function with the specified query.
    extract_videos(query)
