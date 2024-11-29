import streamlit as st
import subprocess

# Function to run scripts
def run_script(script_name):
    try:
        subprocess.run(["python", script_name], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Streamlit UI
st.title('Sentiment Analysis of Reviews')

# Place search input
place = st.text_input("Enter a place name:")

# Button to start the analysis
if st.button('Search'):
    if not place:
        st.error("Please enter a place name.")
    else:
        st.write("Processing...")

        # Run the scripts sequentially
        if run_script('scraper.py'):
            st.write("Scraping completed.")
            if run_script('preprocess.py'):
                st.write("Preprocessing completed.")
                if run_script('sentiment_analysis.py'):
                    st.write("Sentiment Analysis completed.")
                    if run_script('sentiment_analysis_visualizations.py'):
                        st.write("Visualization completed. Check the output!")
                    else:
                        st.error("Visualization generation failed.")
                else:
                    st.error("Sentiment Analysis failed.")
            else:
                st.error("Preprocessing failed.")
        else:
            st.error("Scraping failed.")
