import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def scrape_google_reviews(place_name, review_limit=50):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    reviews = set()

    try:
        print(f"Searching for: {place_name}")
        driver.get("https://www.google.com/maps")
        time.sleep(3)

        # Search for the place
        search_box = driver.find_element(By.ID, "searchboxinput")
        search_box.send_keys(place_name)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)

        print("Locating and clicking the reviews button...")
        try:
            reviews_button = driver.find_element(
                By.XPATH, "//button[contains(., 'reviews')]"
            )
            reviews_button.click()
            time.sleep(5)
        except Exception as e:
            print(f"Error clicking the reviews button: {e}")
            return list(reviews)

        # Scrolling and extracting reviews
        scroll_attempts = 0
        max_scroll_attempts = 15  # Prevent infinite scrolling
        last_height = driver.execute_script("return document.body.scrollHeight")

        while len(reviews) < review_limit and scroll_attempts < max_scroll_attempts:
            # Get all reviews on the current screen
            review_elements = driver.find_elements(By.CLASS_NAME, "wiI7pd")
            if not review_elements:
                print("No reviews found on this load attempt.")
                scroll_attempts += 1
                time.sleep(2)
                continue

            # Add new reviews
            new_reviews = {review.text for review in review_elements if review.text}
            reviews.update(new_reviews)

            print(f"Collected {len(reviews)} reviews so far...")

            # Scroll to the bottom of the container
            driver.execute_script("arguments[0].scrollIntoView();", review_elements[-1])
            time.sleep(2)

            # Check if scrolling reached the end
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("No more content to scroll.")
                break
            last_height = new_height
            scroll_attempts += 1

        # Limit the reviews to the requested number
        reviews = list(reviews)[:review_limit]
        print(f"Extracted {len(reviews)} unique reviews.")
        return reviews

    except Exception as ex:
        print(f"An error occurred: {ex}")
        return list(reviews)

    finally:
        driver.quit()
