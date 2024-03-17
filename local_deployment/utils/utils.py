
import streamlit as st
import re

# Function to determine color based on sentiment score
def get_color(sentiment_score):
    if sentiment_score < 0:
        # Closer to -1, more red
        red = 255
        green = int(255 * (1 + sentiment_score))  # Increase green as score moves to 0
    else:
        # Closer to 1, more green
        green = 255
        red = int(255 * (1 - sentiment_score))  # Decrease red as score moves to 1
    return f'rgb({red}, {green}, 0)'

def show_news(list_news, number_of_news_per_column = 2):
    i = 0
    while True:
        if i>number_of_news_per_column:
            break
        data= list_news[i]
        if not data['banner_image']:
            continue
        st.image(data['banner_image'])  # Display image
        st.markdown(
            f"<h4 style='font-size: medium;'><a href='{data['url']}'>{data['title']}</a></h4>", unsafe_allow_html=True
        )  # Display title as hyperlink
        # Determine color based on sentiment score
        color = get_color(data["overall_sentiment_score"])
        # set a tag
        st.markdown(
            f"<span style='display: inline-block; border: 1px solid #ddd; padding: 5px 10px; border-radius: 5px; background-color: {color};'>{data['overall_sentiment_label']}</span>",
            unsafe_allow_html=True
        )
        st.markdown(re.sub(r'(?<!\$)\$(?!\$)', r'\$', data['summary']))  # Display HTML content
        i+=1