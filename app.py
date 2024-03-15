import streamlit as st
import page1
import page2
import page3
import argparse
import efficient_frontier


parser = argparse.ArgumentParser()

parser.add_argument("-l", "--local", help="if this is local development", default=False, type= bool)

args = parser.parse_args()

if args.local:
    import page1_local
    PAGES = {
        "Market Overview": page1_local,
        "Stock Performance": page3,
        "Efficient Frontier": efficient_frontier
    }

else:
    PAGES = {
        "Market Overview": page1,
        "Stock Performance": page3,
        "Efficient Frontier": efficient_frontier
    }

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()