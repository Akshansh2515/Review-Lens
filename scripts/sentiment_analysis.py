from transformers import pipeline

# Initialize the sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_sentiments(cleaned_reviews):
    try:
        results = sentiment_analyzer(cleaned_reviews)
        sentiments = [result["label"] for result in results]
        confidences = [result["score"] for result in results]
        return sentiments, confidences
    except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        return ["Error"] * len(cleaned_reviews), [0] * len(cleaned_reviews)
