from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse

app = Flask(__name__)
CORS(app)  # enabling cors for every routes

#webdriver configuration
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")  # For better performance in headless mode
chrome_options.add_argument("--no-sandbox")  # To avoid issues on certain systems

# chrome driver ka location
service = Service(r'C:\Users\AYUSH\Downloads\chromedriver-win64\chromedriver.exe')

def get_driver():
    return webdriver.Chrome(service=service, options=chrome_options)

# Supported domains
SUPPORTED_DOMAINS = ["www.croma.com", "www.91mobiles.com", "www.reliancedigital.in"]

def extract_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

def is_supported_domain(domain):
    return domain in SUPPORTED_DOMAINS

@app.route('/compare', methods=['POST'])
def compare_prices():
    try:
        data = request.get_json()
        url1 = data.get('url1')
        url2 = data.get('url2')

        if not url1 or not url2:
            return jsonify({'error': 'Both URLs are required.'}), 400

        # Extract domain from URLs
        domain1 = extract_domain(url1)
        domain2 = extract_domain(url2)

        # domain support check
        if not is_supported_domain(domain1):
            return jsonify({'error': f'Unsupported site for {domain1}. Only Croma, 91mobiles, and Reliance Digital are supported.'}), 400
        if not is_supported_domain(domain2):
            return jsonify({'error': f'Unsupported site for {domain2}. Only Croma, 91mobiles, and Reliance Digital are supported.'}), 400

        # Dynamically determine which scraper to use based on domain
        price1 = (
            scrape_chroma_price(url1) if domain1 == "www.croma.com"
            else scrape_91mobiles_price(url1) if domain1 == "www.91mobiles.com"
            else scrape_reliance_digital_price(url1) if domain1 == "www.reliancedigital.in"
            else None
        )

        price2 = (
            scrape_chroma_price(url2) if domain2 == "www.croma.com"
            else scrape_91mobiles_price(url2) if domain2 == "www.91mobiles.com"
            else scrape_reliance_digital_price(url2) if domain2 == "www.reliancedigital.in"
            else None
        )

        if price1 is None and price2 is None:
            return jsonify({'error': 'Failed to retrieve prices from both sites.'}), 500

        return jsonify({
            'url1_price': price1,
            'url2_price': price2,
            'domain1': domain1,
            'domain2': domain2
        })
    except Exception as e:
        print(f"Error in /compare route: {e}")
        return jsonify({'error': str(e)}), 500


def scrape_chroma_price(url):
    driver = get_driver()
    try:
        driver.get(url)
        print(f"Fetching URL: {url}")

        # Waiting
        WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.ID, 'pdp-product-price'))
        )

        #price element detect karta hai using id
        price_element = driver.find_element(By.ID, 'pdp-product-price')

        # extraction
        price_value = price_element.get_attribute('value')  # Extract from 'value' attribute
        if not price_value:
            # Fall back to text if 'value' attribute doesn't exist
            price_value = price_element.text.strip().replace('₹', '').replace(',', '')

        print(f"Extracted price: {price_value}")

        # Convert to float if valid
        return float(price_value) if price_value and price_value.replace('.', '', 1).isdigit() else None
    except Exception as e:
        print(f"Error retrieving Chroma price: {e}")
        return None
    finally:
        driver.quit()

def scrape_91mobiles_price(url):
    driver = get_driver()
    try:
        driver.get(url)
        print(f"Fetching URL: {url}")

        # Waiting
        WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span.store_prc'))
        )


        price_element = driver.find_element(By.CSS_SELECTOR, 'span.store_prc')

        # priceextractor
        price_text = price_element.get_attribute('data-price').strip().replace(',', '')
        print(f"91mobiles price text: {price_text}")

        # Convert to float if valid
        return float(price_text) if price_text and price_text.replace('.', '', 1).isdigit() else None
    except Exception as e:
        print(f"Error retrieving 91mobiles price: {e}")
        return None
    finally:
        driver.quit()


def scrape_reliance_digital_price(url):
    driver = get_driver()
    try:
        driver.get(url)
        print(f"Fetching URL: {url}")

        # Waiting
        WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span.TextWeb__Text-sc-1cyx778-0.kFBgPo'))
        )


        price_element = driver.find_element(By.CSS_SELECTOR, 'span.TextWeb__Text-sc-1cyx778-0.kFBgPo')

        # Extract
        price_text = price_element.text.strip().replace('₹', '').replace(',', '')

        print(f"Reliance Digital price: {price_text}")

        #float return
        return float(price_text) if price_text and price_text.replace('.', '', 1).isdigit() else None

    except Exception as e:
        print(f"Error retrieving Reliance Digital price: {e}")
        return None

    finally:
        driver.quit()


if __name__ == '__main__':
    app.run(debug=True)
