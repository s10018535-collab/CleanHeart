"""Olive Green & Cream theme for Clean Hearts."""

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap');

.stApp { background: linear-gradient(135deg, #FFF8DC 0%, #FAEBD7 50%, #F5E6C8 100%) !important; }
h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #3E4A2B !important; }

.hero-quote {
    font-family: 'Playfair Display', serif; font-size: 3.2rem; font-weight: 700; font-style: italic;
    color: #3E4A2B; text-align: center; margin: 2rem 0; line-height: 1.2;
    text-shadow: 2px 2px 4px rgba(85, 107, 47, 0.15);
}
.hero-quote::before { content: "\\201C"; font-size: 5rem; color: #6B8E23; vertical-align: -0.3em; margin-right: 0.1em; }
.hero-quote::after  { content: "\\201D"; font-size: 5rem; color: #6B8E23; vertical-align: -0.5em; margin-left: 0.1em; }

.subtitle {
    text-align: center; font-family: 'Inter', sans-serif; color: #6B8E23; font-size: 1.1rem;
    letter-spacing: 3px; text-transform: uppercase; margin-bottom: 1rem;
}

.issue-card {
    background: linear-gradient(145deg, #FFFFFF 0%, #FFF8DC 100%); border-radius: 18px; padding: 0;
    margin: 1rem 0; box-shadow: 0 8px 24px rgba(62, 74, 43, 0.12), 0 2px 6px rgba(62, 74, 43, 0.08);
    overflow: hidden; border: 1px solid rgba(107, 142, 35, 0.15);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.issue-card:hover { transform: translateY(-4px); box-shadow: 0 14px 36px rgba(62, 74, 43, 0.2); }
.card-image { width: 100%; height: 200px; object-fit: cover; display: block; }
.card-body { padding: 1.2rem 1.4rem; }
.card-title { font-family: 'Playfair Display', serif; font-size: 1.3rem; font-weight: 700; color: #3E4A2B; margin: 0 0 0.5rem 0; }
.card-meta { display: flex; gap: 0.8rem; flex-wrap: wrap; margin-top: 0.8rem; }
.badge { display: inline-block; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600; font-family: 'Inter', sans-serif; letter-spacing: 0.5px; }
.badge-sorted   { background: #6B8E23; color: #FFF8DC; }
.badge-pending  { background: #D4A574; color: #3E4A2B; }
.badge-resolved { background: #3E4A2B; color: #FFF8DC; }
.badge-high     { background: #C44536; color: white; }
.badge-medium   { background: #D4A574; color: #3E4A2B; }
.badge-low      { background: #8FBC8F; color: #3E4A2B; }
.badge-domain   { background: #556B2F; color: #FFF8DC; }
.card-desc { font-family: 'Inter', sans-serif; color: #555; font-size: 0.95rem; line-height: 1.5; margin: 0.5rem 0; }
.card-address { font-family: 'Inter', sans-serif; color: #6B8E23; font-size: 0.85rem; font-style: italic; margin-top: 0.5rem; }

section[data-testid="stSidebar"] { background: linear-gradient(180deg, #3E4A2B 0%, #556B2F 100%) !important; }
section[data-testid="stSidebar"] * { color: #FFF8DC !important; }

.stButton > button {
    background: linear-gradient(135deg, #6B8E23 0%, #556B2F 100%) !important; color: #FFF8DC !important;
    border: none !important; border-radius: 30px !important; padding: 0.6rem 2rem !important;
    font-family: 'Inter', sans-serif !important; font-weight: 600 !important; letter-spacing: 1px !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(85, 107, 47, 0.4) !important; }

.stTextInput > div > div > input, .stTextArea > div > div > textarea {
    background-color: #FFFEF5 !important; border: 2px solid #D4C896 !important; border-radius: 10px !important;
    color: #3E4A2B !important; font-family: 'Inter', sans-serif !important;
}
.stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
    border-color: #6B8E23 !important; box-shadow: 0 0 0 3px rgba(107, 142, 35, 0.2) !important;
}

.logo-container { text-align: center; padding: 1rem 0; border-bottom: 2px solid rgba(107, 142, 35, 0.2); margin-bottom: 1.5rem; }
.logo-text { font-family: 'Playfair Display', serif; font-size: 2.2rem; font-weight: 900; color: #3E4A2B; letter-spacing: 4px; }
.logo-leaf { color: #6B8E23; }
.divider { height: 3px; background: linear-gradient(90deg, transparent, #6B8E23, transparent); margin: 2rem 0; border-radius: 2px; }

.stat-card { background: linear-gradient(135deg, #556B2F 0%, #6B8E23 100%); color: #FFF8DC; padding: 1.5rem; border-radius: 16px; text-align: center; box-shadow: 0 6px 18px rgba(62, 74, 43, 0.25); }
.stat-number { font-family: 'Playfair Display', serif; font-size: 2.8rem; font-weight: 900; display: block; }
.stat-label { font-family: 'Inter', sans-serif; font-size: 0.85rem; letter-spacing: 2px; text-transform: uppercase; opacity: 0.9; }

.official-header { background: linear-gradient(135deg, #3E4A2B 0%, #556B2F 100%); color: #FFF8DC; padding: 1.5rem 2rem; border-radius: 16px; margin-bottom: 1.5rem; }
</style>
"""
