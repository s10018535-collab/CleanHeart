import streamlit as st

from config import DEPARTMENTS
from database import list_issues
from views.common import EXCERPT_LENGTH, escape, format_time_ago, status_label


def _issue_card_html(issue: dict) -> str:
    urgent_badge = '<span class="badge badge-urgent">Urgent</span>' if issue["priority"] == "urgent" else ""
    return f"""
    <div class="meta">
      <span class="badge">{escape(issue["department"])}</span>
      <span class="badge badge-{issue["status"]}">{escape(status_label(issue["status"]))}</span>
      {urgent_badge}
      <span>{escape(format_time_ago(issue["created_at"]))}</span>
    </div>
    <div class="title">{escape(issue["title"])}</div>
    <div class="address">{escape(issue["address"])}</div>
    """


def _render_issue_card(issue: dict) -> None:
    description = issue["description"]
    is_long = len(description) > EXCERPT_LENGTH
    excerpt = description[:EXCERPT_LENGTH].rstrip() + "..." if is_long else description

    with st.container(border=True):
        st.image(issue["photo_url"], use_container_width=True)
        st.markdown(_issue_card_html(issue), unsafe_allow_html=True)
        st.markdown(f'<div class="excerpt">{escape(excerpt)}</div>', unsafe_allow_html=True)
        if is_long:
            with st.expander("Read more"):
                st.markdown(escape(description).replace("\n", "<br>"), unsafe_allow_html=True)


def render_updates() -> None:
    st.markdown(
        """
        <div class="hero">
          <span class="eyebrow">Civic reporting, made human</span>
          <h1>Small voices. Big changes.</h1>
          <p>Spotted a problem in your neighborhood? Tell us where it is and we will send it straight to the
          city team that can fix it. Follow every update from here.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Latest from the community")
    filter_col, sort_col = st.columns([2, 1])
    with filter_col:
        department = st.selectbox("Department", ["All", *DEPARTMENTS.keys()])
    with sort_col:
        sort = st.selectbox("Sort posts", ["Newest first", "Urgent first"])

    issues = list_issues(None if department == "All" else department)
    if sort == "Urgent first":
        issues.sort(key=lambda item: item["priority"] != "urgent")

    if not issues:
        st.info("No posts in this department yet. Be the first to report an issue.")
        return

    columns_per_row = 3
    for start in range(0, len(issues), columns_per_row):
        columns = st.columns(columns_per_row)
        for column, issue in zip(columns, issues[start : start + columns_per_row]):
            with column:
                _render_issue_card(issue)
