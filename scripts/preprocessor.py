import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import re

nltk.download('stopwords')
nltk.download('punkt')

STOPWORDS = set(stopwords.words('english'))

def clean_text(text):
    try:
        # Ensure the input is a string
        if not isinstance(text, str):
            print(f"Skipping non-string review: {text}")
            return ""  # Return an empty string if not a valid string
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)  # Remove URLs
        text = re.sub(r'<.*?>', '', text)  # Remove HTML tags
        text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove non-alphabetic characters
        text = text.lower()  # Convert to lowercase
        tokens = word_tokenize(text)  # Tokenize
        tokens = [word for word in tokens if word not in STOPWORDS]  # Remove stopwords
        return ' '.join(tokens)
    except Exception as e:
        print(f"Error cleaning text: {e}")
        return ""  # Return an empty string if error occurs

def preprocess_reviews(reviews):
    try:
        # Ensure the input is a DataFrame
        if not isinstance(reviews, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame.")
        
        # Check that the DataFrame has the 'Original Review' column
        if 'Original Review' not in reviews.columns:
            raise ValueError("The input DataFrame must contain an 'Original Review' column.")
        
        # Apply the clean_text function to preprocess each review
        reviews['Cleaned Review'] = reviews['Original Review'].apply(lambda x: clean_text(x))
        
        # Check if preprocessing was successful
        if reviews['Cleaned Review'].isnull().all():
            print("All reviews were cleaned to empty strings. Exiting.")
            return pd.DataFrame()  # Return an empty DataFrame if all reviews are empty
        
        return reviews
    except Exception as e:
        print(f"Error in preprocessing reviews: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on failure
