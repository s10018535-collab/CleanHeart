import streamlit as st

from auth import verify_officer_password
from config import DEPARTMENTS, STATUS_LABELS
from database import list_issues, update_status
from views.common import escape, format_time_ago, status_label

SESSION_KEY = "officer_department"

NEXT_ACTION = {
    "new": ("in_progress", "Start work"),
    "in_progress": ("resolved", "Mark resolved"),
    "resolved": ("in_progress", "Reopen"),
}


def _render_login() -> None:
    st.title("Officer sign in")
    st.write("This area is for authorised city officials only. Choose your department and enter the officer password.")

    departments = list(DEPARTMENTS)
    with st.form("officer_login"):
        department = st.selectbox("Your department", departments)
        password = st.text_input("Officer password", type="password")
        submitted = st.form_submit_button("Sign in", type="primary")

    if not submitted:
        return
    if not password:
        st.error("Please enter the officer password.")
        return
    if not verify_officer_password(password):
        st.error("Incorrect password.")
        return
    st.session_state[SESSION_KEY] = department
    st.rerun()


def _change_status(issue_id: int, department: str, status: str) -> None:
    if not update_status(issue_id, department, status):
        st.session_state["officer_error"] = "This report is no longer in your department."


def _render_dashboard(department: str) -> None:
    head_col, action_col = st.columns([4, 1])
    with head_col:
        st.title(department)
        st.write("Reports routed to your department. Update each one as work progresses.")
    with action_col:
        if st.button("Sign out", use_container_width=True):
            del st.session_state[SESSION_KEY]
            st.rerun()

    if error := st.session_state.pop("officer_error", None):
        st.error(error)

    issues = list_issues(department)
    counts = {status: sum(1 for issue in issues if issue["status"] == status) for status in STATUS_LABELS}

    status_filter = st.radio(
        "Show reports",
        list(STATUS_LABELS),
        format_func=lambda key: f"{STATUS_LABELS[key]} ({counts[key]})",
        horizontal=True,
    )

    visible = [issue for issue in issues if issue["status"] == status_filter]
    if not visible:
        st.info("No reports with this status right now.")
        return

    for issue in visible:
        with st.container(border=True):
            meta_col, action_col = st.columns([4, 1])
            with meta_col:
                urgent = ' <span class="badge badge-urgent">Urgent</span>' if issue["priority"] == "urgent" else ""
                st.markdown(
                    f'<span class="badge badge-{issue["status"]}">{escape(status_label(issue["status"]))}</span>'
                    f"{urgent} <small>{escape(format_time_ago(issue['created_at']))}</small>",
                    unsafe_allow_html=True,
                )
                st.markdown(f"**{escape(issue['title'])}**", unsafe_allow_html=True)
                st.markdown(f"<small>{escape(issue['address'])}</small>", unsafe_allow_html=True)
                st.markdown(escape(issue["description"]).replace("\n", "<br>"), unsafe_allow_html=True)
            with action_col:
                next_status, label = NEXT_ACTION[issue["status"]]
                st.button(
                    label,
                    key=f"issue-{issue['id']}",
                    type="primary",
                    use_container_width=True,
                    on_click=_change_status,
                    args=(issue["id"], department, next_status),
                )


def render_officer() -> None:
    department = st.session_state.get(SESSION_KEY)
    if department is None:
        _render_login()
    else:
        _render_dashboard(department)
