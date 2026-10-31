import streamlit as st

_CSS = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600&family=Fraunces:opsz,wght@9..144,600&display=swap');

:root {
  --pink-600: #a05e5e;
  --pink-700: #824a4b;
  --pink-800: #633838;
  --pink-100: #f6e6e5;
  --cream-100: #fbf6ee;
  --cream-300: #e9dcc7;
  --ink-700: #5b4b48;
}

html, body, [class*="css"] {
  font-family: 'DM Sans', system-ui, sans-serif;
  color: #2e2423;
}

.stApp {
  background: var(--cream-100);
}

h1, h2, h3 {
  font-family: 'Fraunces', Georgia, serif !important;
  font-weight: 600 !important;
  color: #2e2423;
  line-height: 1.2 !important;
}

header[data-testid="stHeader"] {
  background: transparent;
}

.hero {
  text-align: center;
  padding: 56px 16px 40px;
  background:
    radial-gradient(circle at 15% 20%, #ecd0ce 0, transparent 35%),
    radial-gradient(circle at 85% 10%, #e9dcc7 0, transparent 30%);
  border-radius: 24px;
  margin-bottom: 32px;
  animation: fade-up 0.8s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.hero .eyebrow {
  display: inline-block;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--pink-700);
  margin-bottom: 16px;
}

.hero h1 {
  font-size: clamp(44px, 7vw, 72px) !important;
  color: var(--pink-800) !important;
  margin: 0;
}

.hero p {
  max-width: 560px;
  margin: 24px auto 0;
  font-size: 18px;
  color: var(--ink-700);
}

.meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  font-size: 13px;
  color: #7a6a66;
  margin-bottom: 8px;
}

.title {
  font-family: 'Fraunces', Georgia, serif;
  font-size: 20px;
  font-weight: 600;
  line-height: 1.25;
  margin-bottom: 8px;
}

.address {
  font-size: 14px;
  color: var(--ink-700);
  margin-bottom: 8px;
}

.excerpt {
  font-size: 15px;
  color: var(--ink-700);
}

.badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  background: var(--pink-100);
  color: var(--pink-800);
}

.badge-new { background: #fcebc9; color: #7a4e00; }
.badge-in_progress { background: var(--pink-100); color: var(--pink-800); }
.badge-resolved { background: #e4ede6; color: #4f6f5b; }
.badge-urgent { background: #f9e3e1; color: #9b2f2f; }

.stButton > button, .stFormSubmitButton > button {
  border-radius: 999px;
  font-weight: 600;
  min-height: 44px;
  transition: transform 0.2s ease, background 0.2s ease;
}

.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {
  background: var(--pink-600);
  border-color: var(--pink-600);
  color: #ffffff;
}

.stButton > button[kind="primary"]:hover, .stFormSubmitButton > button[kind="primary"]:hover {
  background: var(--pink-700);
  border-color: var(--pink-700);
  color: #ffffff;
  transform: translateY(-1px);
}

.stButton > button[kind="secondary"]:hover {
  border-color: var(--pink-600);
  color: var(--pink-800);
}

@keyframes fade-up {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; }
}
"""


def apply_theme() -> None:
    st.markdown(f"<style>{_CSS}</style>", unsafe_allow_html=True)
