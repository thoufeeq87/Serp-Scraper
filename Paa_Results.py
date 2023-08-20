# Importing necessary libraries:
# - `sync_playwright`: For web automation, fetching dynamic content from web pages.
# - `pandas`: For data manipulation and saving data as CSV.
from playwright.sync_api import sync_playwright
import pandas as pd

# Function to fetch the People Also Ask (PAA) questions from Google search results.
def fetch_paa_results(query):
    # Initializing Playwright context.
    with sync_playwright() as p:
        # Launching a Chromium browser instance.
        browser = p.chromium.launch()
        # Opening a new tab or page.
        page = browser.new_page()

        # Navigating to Google's search page with the given query.
        page.goto(f"https://www.google.com/search?q={query}")

        # Loop to click and expand the PAA questions. We aim to click on the first four.
        for i in range(4):
            # Identifying the next PAA question using the provided CSS selector.
            question_to_click = page.query_selector('div.related-question-pair span.CSkcDe')
            # If an question is found, click on it.
            if question_to_click:
                question_to_click.click()
                # Waiting for a second to allow any dynamic content to load.
                page.wait_for_timeout(1000)

        # Fetching all expanded PAA questions after the clicks.
        paa_boxes = page.query_selector_all("div.related-question-pair")
        # Extracting the text content of the fetched PAA questions.
        questions = [box.query_selector("span.CSkcDe").inner_text() for box in paa_boxes if box]

        # Closing the browser instance.
        browser.close()
        # Returning the list of PAA questions.
        return questions

# Main execution block.
if __name__ == "__main__":
    # Specifying the search query for which we want to fetch PAA questions.
    query = "web scraping"
    # Calling the fetch_paa_results function to gather PAA questions for the specified query.
    paa_questions = fetch_paa_results(query)

    # Converting the list of PAA questions to a pandas DataFrame.
    df = pd.DataFrame(paa_questions, columns=["PAA Questions"])

    # Saving the DataFrame to a CSV file. The file name is based on the search query.
    file_name = f"{query}_paa_results.csv"
    df.to_csv(file_name, index=False)
    # Providing feedback on where the results are saved.
    print(f"Saved results to {file_name}")
