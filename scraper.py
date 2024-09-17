import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# Function to get reviews from a specific product page
def get_reviews(product_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    # Send HTTP request
    response = requests.get(product_url, headers=headers)
    
    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Create a list to store reviews
    reviews_list = []
    
    # Find the review section (customize according to the site's structure)
    reviews = soup.find_all('div', class_='review')

    # Extract necessary data from each review
    for review in reviews:
        review_title = review.find('h2', class_='review-title').text.strip()
        review_rating = review.find('span', class_='review-rating').text.strip()
        review_text = review.find('p', class_='review-text').text.strip()
        review_date = review.find('span', class_='review-date').text.strip()

        reviews_list.append({
            'Title': review_title,
            'Rating': review_rating,
            'Review': review_text,
            'Date': review_date
        })
        
    return reviews_list

# Function to handle multiple pages
def scrape_reviews(url_template, total_pages):
    all_reviews = []
    
    for page in range(1, total_pages + 1):
        print(f"Scraping page {page}")
        url = url_template.format(page)
        reviews = get_reviews(url)
        all_reviews.extend(reviews)
        
        # Sleep randomly to avoid being blocked
        time.sleep(random.uniform(2, 5))
    
    return all_reviews

# Example Usage
product_url_template = 'https://example.com/product-reviews?page={}'  # Placeholder URL
total_pages = 5  # Set the total number of pages

reviews_data = scrape_reviews(product_url_template, total_pages)

# Convert the list to a DataFrame and save it as a CSV
df = pd.DataFrame(reviews_data)
df.to_csv('customer_reviews.csv', index=False)

print("Scraping complete. Data saved to customer_reviews.csv")
