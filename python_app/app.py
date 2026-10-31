import streamlit as st

from database import init_db
from theme import apply_theme
from views.officer import render_officer
from views.report import render_report
from views.updates import render_updates

PAGES = {
    "Updates": render_updates,
    "Report an issue": render_report,
    "Officer portal": render_officer,
}


@st.cache_resource
def _setup_database() -> None:
    init_db()


st.set_page_config(page_title="CLEAN HEARTS", layout="wide")
_setup_database()
apply_theme()

with st.sidebar:
    st.markdown("### CLEAN HEARTS")
    st.caption("Small voices. Big changes.")
    page = st.radio("Go to", list(PAGES), label_visibility="collapsed")

PAGES[page]()
