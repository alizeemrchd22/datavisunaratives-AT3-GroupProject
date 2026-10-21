import streamlit as st

st.set_page_config(page_title="Is AI concentrating?", layout="wide")

pages = [
    st.Page("sections/home.py", title="The question", default=True),
    st.Page("sections/story1.py", title="1. A few companies dominate"),
    st.Page("sections/story2.py", title="2. The field is opening up"),
    st.Page("sections/story3.py", title="3. It depends what you count"),
    st.Page("sections/conclusion.py", title="Our answer"),
]

st.navigation(pages).run()
