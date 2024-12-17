import streamlit as st
import re
import PyPDF2
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

# Predefined Hawkish/Dovish Words for Classification
hawkish_terms = {
    "tighten": 1, "inflation": 1, "rate hike": 2, "restrictive policy stance": 2,
    "elevated inflation": 2, "tight financial conditions": 2, "labor market tightness": 1
}
dovish_terms = {
    "accommodative": 1, "stimulus": 1, "easing": 1, "economic cooling": 2,
    "slowing economic activity": 2, "lower unemployment risks": 1, "supply-demand pressures easing": 2
}

# Clean text
def clean_text(text):
    text = re.sub(r"\s+", " ", text)  # Remove extra whitespaces
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove special characters
    text = text.lower()  # Convert to lowercase
    return text

# Sentiment Classification
def classify_sentiment(text):
    cleaned_text = clean_text(text)
    hawkish_score = sum(cleaned_text.count(term) * weight for term, weight in hawkish_terms.items())
    dovish_score = sum(cleaned_text.count(term) * weight for term, weight in dovish_terms.items())

    if hawkish_score > dovish_score:
        return "Hawkish", hawkish_score, dovish_score
    elif dovish_score > hawkish_score:
        return "Dovish", hawkish_score, dovish_score
    else:
        return "Neutral", hawkish_score, dovish_score

# Extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Streamlit App
st.title("📊 FOMC Sentiment Analysis Tool")
st.markdown("""
Analyze FOMC meeting minutes to assess the Hawkish or Dovish sentiment.  
Upload a document, and we'll do the rest! 🚀
""")

# File Upload
uploaded_file = st.file_uploader("Upload a file (TXT or PDF format)", type=["txt", "pdf"])

if uploaded_file:
    # Progress Bar
    progress_bar = st.progress(0)
    progress_bar.progress(20)

    # Determine file type and extract text
    if uploaded_file.name.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith(".pdf"):
        text = extract_text_from_pdf(uploaded_file)
    else:
        st.error("Unsupported file format.")
        st.stop()

    progress_bar.progress(50)

    # Check if text was extracted
    if not text.strip():
        st.error("No text could be extracted from the uploaded file. Please ensure the file contains readable text.")
        st.stop()

    # Sentiment Analysis
    sentiment, hawkish_score, dovish_score = classify_sentiment(text)
    progress_bar.progress(75)

    # Display Results
    st.subheader(f"📈 Sentiment Analysis Result: **{sentiment}**")
    st.write(f"- **Hawkish Score:** {hawkish_score}")
    st.write(f"- **Dovish Score:** {dovish_score}")

    # Word Cloud Section (Moved Up)
    st.subheader("Word Cloud of Uploaded Document")
    cleaned_text = clean_text(text)
    if cleaned_text.strip():
        wordcloud = WordCloud(background_color="white", width=800, height=400).generate(cleaned_text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        st.pyplot(plt)
    else:
        st.error("Unable to generate a word cloud as the cleaned text is empty.")

    # Dynamic Bar Chart for Scores
    st.subheader("Sentiment Score Comparison")
    score_df = pd.DataFrame({
        "Sentiment": ["Hawkish", "Dovish"],
        "Score": [hawkish_score, dovish_score]
    })
    fig = px.bar(
        score_df, x="Sentiment", y="Score", color="Sentiment",
        title="Sentiment Score Comparison",
        color_discrete_map={"Hawkish": "#FF6347", "Dovish": "#4682B4"}
    )
    st.plotly_chart(fig)

    progress_bar.progress(90)

    # Keyword Analysis
    st.subheader("Keyword Frequency Analysis")
    hawkish_found = {term: cleaned_text.count(term) for term in hawkish_terms if term in cleaned_text}
    dovish_found = {term: cleaned_text.count(term) for term in dovish_terms if term in cleaned_text}

    hawkish_df = pd.DataFrame(list(hawkish_found.items()), columns=["Term", "Frequency"])
    dovish_df = pd.DataFrame(list(dovish_found.items()), columns=["Term", "Frequency"])

    st.write("**Hawkish Terms Found:**")
    st.table(hawkish_df)

    st.write("**Dovish Terms Found:**")
    st.table(dovish_df)

    progress_bar.progress(100)
