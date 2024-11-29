import matplotlib.pyplot as plt

def visualize_analysis(df):
    # Sentiment distribution
    sentiment_counts = df["Sentiment"].value_counts()

    # Create a pie chart using Matplotlib
    fig, ax = plt.subplots(figsize=(6, 4))  # Explicitly create the figure and axes
    ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90, colors=['skyblue', 'lightgreen', 'salmon'])
    
    ax.set_title("Sentiment Distribution of Reviews", fontsize=16)
    
    # Return the figure object for Streamlit to display
    return fig
