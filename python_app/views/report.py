import streamlit as st

from config import DEPARTMENTS
from database import insert_issue
from triage import triage_report
TITLE_RANGE = (3, 120)
DESCRIPTION_RANGE = (10, 2000)
ADDRESS_RANGE = (5, 200)


def _validation_error(title: str, description: str, address: str) -> str | None:
    if not TITLE_RANGE[0] <= len(title) <= TITLE_RANGE[1]:
        return f"Please give the issue a short title (between {TITLE_RANGE[0]} and {TITLE_RANGE[1]} characters)."
    if not DESCRIPTION_RANGE[0] <= len(description) <= DESCRIPTION_RANGE[1]:
        return f"Please describe the problem in a little more detail (at least {DESCRIPTION_RANGE[0]} characters)."
    if not ADDRESS_RANGE[0] <= len(address) <= ADDRESS_RANGE[1]:
        return "Please add the street address or nearest landmark."
    return None


def render_report() -> None:
    st.title("Tell us what needs fixing")
    st.write(
        "Describe the problem and where it is. Your report goes straight to the team responsible for it, "
        "and it appears on the updates page for neighbors to see."
    )

    with st.form("report_form", clear_on_submit=False):
        title = st.text_input("What is the problem?", max_chars=TITLE_RANGE[1], placeholder="e.g. Deep pothole on Maple Avenue")
        description = st.text_area(
            "Tell us more",
            max_chars=DESCRIPTION_RANGE[1],
            height=160,
            placeholder="What is happening, how long has it been there, and who it affects?",
        )
        address = st.text_input(
            "Where is it?",
            max_chars=ADDRESS_RANGE[1],
            placeholder="Street address or nearest landmark",
        )
        submitted = st.form_submit_button("Send report", type="primary")

    if not submitted:
        return

    title = title.strip()
    description = description.strip()
    address = address.strip()
    problem = _validation_error(title, description, address)
    if problem:
        st.error(problem)
        return

    with st.spinner("Routing your report to the right team..."):
        result = triage_report(title, description)

    photo_url = DEPARTMENTS[result.department]["photo"]
    insert_issue(
        title=title,
        description=description,
        address=address,
        department=result.department,
        priority=result.priority,
        photo_url=photo_url,
    )

    urgent_note = " It has been marked urgent so the team can prioritise it." if result.priority == "urgent" else ""
    st.success(f"Thank you, your voice matters. Your report was sent to {result.department}.{urgent_note}")
