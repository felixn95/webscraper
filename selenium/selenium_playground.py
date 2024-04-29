from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.chrome import ChromeDriverManager
# Set up the Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the URL
url = f'https://www.decathlon.de/herren/sportschuhe'
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Accept cookies
try:
    accept_button = driver.find_element(By.ID, 'didomi-notice-agree-button')
    accept_button.click()
except Exception as e:
    print("Cookie button not found:", e)

# Wait for potential page reloads
time.sleep(2)

# Click to open Filialsuche
try:
    search_button = driver.find_element(By.XPATH, '//button[@aria-label="Verwende meinen Standort"]')
    search_button.click()
except Exception as e:
    print("Search button not found:", e)

# Enter a zip code
try:
    search_input = driver.find_element(By.ID, 'autocomplete-input')
    search_input.send_keys('97070')
    search_input.send_keys(Keys.RETURN)
except Exception as e:
    print("Input field not found:", e)

# Wait for search results to load
time.sleep(5)

# Select the first store entry
try:
    first_entry_button = driver.find_element(By.XPATH, '//li[@data-id-store][1]/button')
    first_entry_button.click()
except Exception as e:
    print("First store entry button not found:", e)

# Optional: Retrieve and print details of the selected store
try:
    store_details = driver.find_element(By.XPATH, '//li[@data-id-store][1]')
    print(store_details.text)
except Exception as e:
    print("Store details not found:", e)

# Clean up, close the browser
driver.quit()
