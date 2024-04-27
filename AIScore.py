from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import undetected_chromedriver as uc
import time

# Set up the Chrome WebDriver
options = uc.ChromeOptions()
options.headless = False
options.add_argument("--window-size=1920,1080")
options.binary_location = r"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
driver = uc.Chrome(driver_executable_path=r"/usr/local/bin/chromedriver", options=options)

driver.get("https://www.aiscore.com/")

# Click the Football tab
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Football']"))).click()
time.sleep(1)

scheduled_tab = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Scheduled']")))
driver.execute_script("arguments[0].click();", scheduled_tab)
time.sleep(1)

def scrape_match_urls():
    urls_collected = []
    unique_check = set()
    retry_count = 0
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(4)

        matches = driver.find_elements(By.CSS_SELECTOR, "a[data-id][href*='/h2h']")
        current_count = len(urls_collected)
        for match in matches:
            url = match.get_attribute('href')
            if url not in unique_check:
                unique_check.add(url)
                urls_collected.append(url)

        if len(urls_collected) == current_count:
            retry_count += 1
            if retry_count > 3:  # Allow a few retries before stopping
                break
        else:
            retry_count = 0  # Reset retry count on new data

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height and retry_count > 3:
            break  # Confirm the bottom is reached after retries
        last_height = new_height

    return urls_collected

# Using the function to get all match URLs
urls = scrape_match_urls()
for url in urls:
    print(url)

# Close the driver
driver.quit()






