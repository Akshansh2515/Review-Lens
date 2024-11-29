import os
import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from transformers import pipeline
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import nltk

# Set up NLTK
nltk.data.path.append("C:/Users/ASUS/AppData/Roaming/nltk_data")  # Adjust this path as needed
nltk.download('stopwords')
nltk.download('punkt', force=True)
nltk.download('wordnet')

# Initialize NLP tools
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

# Initialize sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis")


def preprocess_reviews(reviews):
    """
    Cleans and preprocesses a list of reviews.
    """
    def clean_review(text):
        if pd.isna(text):  # Handle missing or NaN values
            return ""
        # Remove unwanted characters but retain sentiment indicators like '!', '?'
        text = re.sub(r"[^a-zA-Z\s!?]", "", text)
        text = text.lower()
        words = word_tokenize(text)
        words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
        return " ".join(words)

    return [clean_review(review) for review in reviews]


def scrape_google_reviews(place_name):
    """
    Scrapes Google reviews for a given place using Selenium.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    try:
        print(f"Searching for: {place_name}")
        driver.get("https://www.google.com/maps")
        time.sleep(2)

        search_box = driver.find_element(By.ID, "searchboxinput")
        search_box.send_keys(place_name)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)

        print("Locating and clicking the reviews button...")
        try:
            reviews_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]")
            reviews_button.click()
            time.sleep(10)
        except Exception as e:
            print(f"Error clicking the reviews button: {e}")
            return []

        reviews = []
        while len(reviews) < 50:
            review_elements = driver.find_elements(By.CLASS_NAME, "wiI7pd")
            for review in review_elements:
                reviews.append(review.text)

            if len(review_elements) > 0:
                driver.execute_script("arguments[0].scrollIntoView();", review_elements[-1])
            else:
                print("No more reviews to load.")
                break
            time.sleep(5)

        reviews = list(set(reviews))[:50]
        print(f"Extracted {len(reviews)} reviews.")
        return reviews
    except Exception as ex:
        print(f"An error occurred: {ex}")
        return []
    finally:
        driver.quit()


def analyze_sentiments(reviews):
    """
    Analyzes sentiments of the given reviews.
    """
    sentiments = []
    confidences = []
    for review in reviews:
        try:
            result = sentiment_analyzer(review)[0]
            sentiments.append(result["label"])
            confidences.append(result["score"])
        except Exception as e:
            print(f"Error analyzing sentiment for review: {e}")
            sentiments.append("Error")
            confidences.append(0)
    return sentiments, confidences


def visualize_analysis(df):
    """
    Visualizes the sentiment analysis results.
    """
    # Pie chart for sentiment distribution
    sentiment_counts = df['Sentiment'].value_counts()

    plt.figure(figsize=(8, 8))
    plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140, colors=["#4CAF50", "#FF5733", "#FFC107"])
    plt.title("Sentiment Distribution of Reviews")
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

    # Histogram for confidence scores
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Confidence'], kde=True, color='blue')
    plt.title("Confidence Distribution of Sentiment Analysis")
    plt.xlabel("Confidence Score")
    plt.ylabel("Frequency")
    plt.show()

    # Word cloud for frequent words in cleaned reviews
    text = " ".join(review for review in df['Cleaned Review'])
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # Turn off the axis
    plt.title("Word Cloud of Reviews")
    plt.show()


def scrape_preprocess_analyze_visualize(place_name):
    """
    Scrapes reviews, preprocesses them, performs sentiment analysis, and visualizes the results.
    """
    reviews = scrape_google_reviews(place_name)
    if not reviews:
        print("No reviews found.")
        return

    # Preprocess reviews
    cleaned_reviews = preprocess_reviews(reviews)

    # Perform sentiment analysis
    sentiments, confidences = analyze_sentiments(cleaned_reviews)

    # Create a DataFrame to store the results
    data = {
        "Original Review": reviews,
        "Cleaned Review": cleaned_reviews,
        "Sentiment": sentiments,
        "Confidence": confidences
    }
    df = pd.DataFrame(data)

    # Save to CSV
    output_dir = "data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    file_path = os.path.join(output_dir, f"{place_name.replace(' ', '_')}_final_reviews.csv")
    df.to_csv(file_path, index=False, encoding="utf-8")
    print(f"Results saved to {file_path}")

    # Visualize the analysis
    visualize_analysis(df)


# Run the script
if __name__ == "__main__":
    place = input("Enter the place you want to scrape reviews for: ")
    scrape_preprocess_analyze_visualize(place)
