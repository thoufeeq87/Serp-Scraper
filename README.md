Copy code
# SERP Scraper

This repository contains scripts designed to scrape search results from Google's SERP (Search Engine Results Page). The tools fetch various search results, such as organic results, images, videos, and People Also Ask (PAA) questions.

## Features
- **Retrieves extensive search results details**:
  - **Organic Search Results**: Fetches the title, URL, and meta description.
  - **Image Search Results**: Retrieves the URL and title of images.
  - **Video Search Results**: Grabs the title and URL of video results.
  - **PAA (People Also Ask) Results**: Expands and fetches the PAA questions.
- Employs the Playwright library for web automation and Selectolax for HTML parsing.
- Directly navigates to the desired type of search results, making it more efficient.
- **Example configuration**: Searches for "web scraping tools". Configurations are modifiable as per user needs.

## 📦 Dependencies
- Playwright
- Selectolax
- pandas

## 🚀 Usage

### Setup:
1. Install the required packages:
   ```bash
   pip install playwright selectolax pandas
2. Navigate to the directory of the desired scraper.

### Run the Script:
- For organic results:
  ```python
  python organic_scraper.
- For image results:
  ```bash
  python image_scraper.py
... and so on for videos and PAA results.

### Output:
Data is saved with a filename pattern, e.g., "query_organic_results.csv", where "query" is your chosen search term.

## 💬 Contributing
Pull requests, feedback, and suggestions are welcome! If you encounter any issues or have questions, please open an issue.


