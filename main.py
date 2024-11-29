import streamlit as st
import os
import pandas as pd
from scripts.scraper1 import scrape_google_reviews
from scripts.preprocessor import preprocess_reviews
from scripts.sentiment_analysis import analyze_sentiments
from scripts.visualizer import visualize_analysis
import matplotlib.pyplot as plt

def main():
    # Step 1: Get user input for the place name
    place_name = st.text_input("Enter the place you want to scrape reviews for:")

    if not place_name:
        st.warning("Please enter a place name.")
        return

    # Step 2: Scrape reviews
    reviews = scrape_google_reviews(place_name)
    
    if not reviews or len(reviews) == 0:
        st.error("No reviews found. Please try another place.")
        return

    # Step 3: Preprocess reviews
    try:
        reviews_df = pd.DataFrame({"Original Review": reviews})
        cleaned_reviews_df = preprocess_reviews(reviews_df)

        if cleaned_reviews_df.empty:
            st.error("No valid reviews after preprocessing. Exiting.")
            return

        cleaned_reviews_list = cleaned_reviews_df["Cleaned Review"].tolist()
    except Exception as e:
        st.error(f"Error during preprocessing: {e}")
        return

    # Step 4: Perform sentiment analysis
    try:
        sentiments, confidences = analyze_sentiments(cleaned_reviews_list)
    except Exception as e:
        st.error(f"Error during sentiment analysis: {e}")
        return

    # Step 5: Create a DataFrame
    df = pd.DataFrame({
        "Original Review": reviews,
        "Cleaned Review": cleaned_reviews_list,
        "Sentiment": sentiments,
        "Confidence": confidences
    })

    # Step 6: Display results DataFrame
    st.write("### Reviews Analysis")
    st.dataframe(df)

    # Step 7: Save results to CSV
    output_dir = "data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    file_path = os.path.join(output_dir, f"{place_name.replace(' ', '_')}_final_reviews.csv")
    df.to_csv(file_path, index=False, encoding="utf-8")
    st.success(f"Results saved to {file_path}")

    # Step 8: Visualize results using Matplotlib pie chart
    st.write("### Visualizing results")
    try:
        fig = visualize_analysis(df)  
        st.pyplot(fig)  
    except Exception as e:
        st.error(f"Error during visualization: {e}")
        return

if __name__ == "__main__":
    main()
