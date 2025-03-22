import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("API_URL")

st.title("News Analyzer")

company = st.text_input("Enter a company name:", "")

if st.button("Analyze News"):
    if company:
        with st.spinner("Loading..."):
            response = requests.get(API_URL, params={"company": company}, stream=True)

            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        data = eval(line.decode("utf-8"))
                        if "status" in data:
                            st.write(f"**Status:** {data['status']}")

                        if "articles" in data:
                            st.subheader("Summarized Articles")
                            for i, article in enumerate(data["articles"]):
                                st.markdown(f"### Article {i+1}")
                                st.write(f"**Title:** {article['title']}")
                                st.write(f"**Summary:** {article['summary']}")
                                st.write(f"**Topics:** {', '.join(article['topics'])}")
                                st.write(f"**Sentiment:** {article['sentiment']}")
                                st.write(f"[Read more]({article['url']})")
                                st.write("---")

                        if "comparative_sentiment_score" in data:
                            st.subheader("Comparative Analysis")

                            st.write("### Sentiment Distribution")
                            sentiment_dist = data["comparative_sentiment_score"]["sentiment_distribution"]
                            st.write(f"- **Positive:** {sentiment_dist['Positive']}")
                            st.write(f"- **Negative:** {sentiment_dist['Negative']}")
                            st.write(f"- **Neutral:** {sentiment_dist['Neutral']}")

                            st.write("### Coverage Differences")
                            for item in data["comparative_sentiment_score"]["coverage_differences"]:
                                st.write(f"**Comparison:** {item['comparison']}")
                                st.write(f"**Impact:** {item['impact']}")
                                st.write("---")

                            st.write("### Common Topics Across Articles")
                            st.write(", ".join(data["comparative_sentiment_score"]["topic_overlap"]))

                        if "final_sentiment_analysis" in data:
                            st.subheader("Overall Sentiment")
                            st.write(data["final_sentiment_analysis"])

                        if "audio" in data:
                            st.subheader("Hindi Audio Summary")
                            st.audio(data["audio"])

            else:
                st.error("Failed to retrieve data. Please try again.")
    else:
        st.warning("Please enter a company name.")
