"""
CLEAN HEARTS — Civic Complaint Triage & Routing Platform
Built with: Streamlit, SQLite, Sentence-Transformers, Python
Theme: Olive Green & Cream
"""

import hashlib
import hmac
import html
import logging
import os
import sqlite3
from urllib.parse import urlparse

import streamlit as st

from theme import THEME_CSS

try:
    from sentence_transformers import SentenceTransformer, util
except Exception:  # library missing -> keyword fallback
    SentenceTransformer = None
    util = None

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("clean_hearts")

DB_NAME = "clean_hearts.db"
CONFIDENCE_THRESHOLD = 25.0  # % below which an issue needs manual review
UNASSIGNED = "Unassigned"
PLACEHOLDER_IMG = (
    "data:image/svg+xml;utf8,"
    "<svg xmlns='http://www.w3.org/2000/svg' width='600' height='200'>"
    "<rect width='100%25' height='100%25' fill='%236B8E23'/>"
    "<text x='50%25' y='50%25' fill='%23FFF8DC' font-size='28' text-anchor='middle'>Clean Hearts</text></svg>"
)


# ============================================================
# 1. DATABASE
# ============================================================
def get_conn():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(pw, salt=None):
    """PBKDF2-HMAC-SHA256 with per-user salt. Returns 'salt$hash' (hex)."""
    salt = salt or os.urandom(16).hex()
    digest = hashlib.pbkdf2_hmac("sha256", pw.encode(), bytes.fromhex(salt), 120_000).hex()
    return f"{salt}${digest}"


def check_password(pw, stored):
    try:
        salt, _ = stored.split("$", 1)
    except ValueError:
        return False
    return hmac.compare_digest(hash_password(pw, salt), stored)


@st.cache_resource
def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            address TEXT NOT NULL,
            category TEXT,
            image_url TEXT,
            status TEXT DEFAULT 'pending',
            priority TEXT DEFAULT 'medium',
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            sorted_by TEXT,
            domain TEXT,
            resolution_notes TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS officials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            domain TEXT NOT NULL,
            email TEXT UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

    c.execute("SELECT COUNT(*) FROM officials")
    if c.fetchone()[0] == 0:
        # Default password comes from env var; override in production.
        default_pw = os.environ.get("OFFICIAL_DEFAULT_PASSWORD", "Govt@123")
        officials = [
            ("Rajesh Kumar", "Sanitation & Waste", "sanitation@gov.in"),
            ("Priya Sharma", "Roads & Infrastructure", "roads@gov.in"),
            ("Amit Verma", "Water Supply", "water@gov.in"),
            ("Sneha Patel", "Electricity & Power", "electricity@gov.in"),
            ("Dr. Manoj Singh", "Public Health", "health@gov.in"),
            ("Kavita Reddy", "Parks & Environment", "parks@gov.in"),
        ]
        c.executemany(
            "INSERT INTO officials (name, domain, email, password_hash) VALUES (?, ?, ?, ?)",
            [(n, d, e, hash_password(default_pw)) for n, d, e in officials],
        )
        conn.commit()

    c.execute("SELECT COUNT(*) FROM issues")
    if c.fetchone()[0] == 0:
        samples = [
            ("Overflowing garbage bin", "The garbage bin at sector 12 market has been overflowing for 3 days. Stray animals are scattering waste on the road.",
             "Sector 12 Market, Near Bus Stand, Delhi", "Sanitation & Waste",
             "https://images.unsplash.com/photo-1605600659908-0ef7b9433d5f?w=600", "sorted", "high"),
            ("Pothole on Main Road", "A large pothole has formed near the school zone. Two accidents reported this week.",
             "MG Road, Block C, Mumbai", "Roads & Infrastructure",
             "https://images.unsplash.com/photo-1515162816999-a0c47dc19247?w=600", "sorted", "high"),
            ("Water leakage from pipe", "Continuous water leakage from the main pipeline wasting thousands of litres daily.",
             "Green Park Colony, Pune", "Water Supply",
             "https://images.unsplash.com/photo-1584824486509-112e4181ff6b?w=600", "pending", "medium"),
            ("Street light not working", "Three street lights on this road have been non-functional for over a week.",
             "Rose Lane, Sector 5, Bangalore", "Electricity & Power",
             "https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=600", "pending", "low"),
            ("Stagnant water breeding mosquitoes", "Stagnant water near the drain is causing a mosquito menace. Dengue risk.",
             "Old City Area, Hyderabad", "Public Health",
             "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=600", "sorted", "high"),
            ("Broken park bench & litter", "Public park benches broken and plastic litter everywhere. Children cannot play safely.",
             "Nehru Park, Chennai", "Parks & Environment",
             "https://images.unsplash.com/photo-1519331379826-f10be5486c6f?w=600", "pending", "medium"),
        ]
        # BUG FIX: also set `domain` so officials can see seeded issues.
        c.executemany(
            "INSERT INTO issues (title, description, address, category, image_url, status, priority, domain) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [s + (s[3],) for s in samples],
        )
        conn.commit()

    # Repair existing DBs created by the old version.
    c.execute("UPDATE issues SET domain=category WHERE (domain IS NULL OR domain='') AND category IS NOT NULL")
    conn.commit()
    conn.close()
    return True


# ============================================================
# 2. AI TRIAGE
# ============================================================
DOMAIN_KEYWORDS = {
    "Sanitation & Waste": ["garbage", "waste", "trash", "dustbin", "litter", "sewage overflow", "cleaning", "sanitation", "bin", "refuse"],
    "Roads & Infrastructure": ["road", "pothole", "street damage", "footpath", "bridge", "construction", "manhole", "asphalt"],
    "Water Supply": ["water", "leakage", "pipe", "supply", "drinking water", "tanker", "waterlogging"],
    "Electricity & Power": ["electricity", "light", "power", "wire", "pole", "transformer", "current", "street light"],
    "Public Health": ["mosquito", "dengue", "disease", "health", "stagnant", "drain", "hospital", "clinic", "hygiene"],
    "Parks & Environment": ["park", "tree", "garden", "bench", "green", "environment", "playground", "plants"],
}

DOMAIN_DESCRIPTIONS = {
    "Sanitation & Waste": "Garbage, trash, waste, litter, overflowing dustbins, sewage overflow and cleaning problems",
    "Roads & Infrastructure": "Damaged roads, potholes, footpaths, bridges, open manholes and construction problems",
    "Water Supply": "Drinking water shortage, pipe leakage, water tankers and water supply problems",
    "Electricity & Power": "Street lights not working, power cuts, loose wires, electric poles and transformers",
    "Public Health": "Mosquitoes, dengue, stagnant water, disease outbreaks, hygiene, hospitals and clinics",
    "Parks & Environment": "Parks, trees, gardens, broken benches, playgrounds and environmental damage",
}


@st.cache_resource
def load_model():
    if SentenceTransformer is None:
        return None
    try:
        return SentenceTransformer('all-MiniLM-L6-v2')
    except Exception:
        log.exception("Model load failed; falling back to keyword matching")
        return None


@st.cache_resource
def domain_embeddings():
    model = load_model()
    if model is None:
        return None
    names = list(DOMAIN_DESCRIPTIONS)
    embs = model.encode([DOMAIN_DESCRIPTIONS[n] for n in names], convert_to_tensor=True)
    return names, embs


def keyword_scores(text):
    low = text.lower()
    return {d: sum(1 for k in kws if k in low) for d, kws in DOMAIN_KEYWORDS.items()}


def triage_issue(title, description):
    """Return (domain, confidence %). Domain is UNASSIGNED when unsure."""
    text = f"{title}. {description}"
    model = load_model()
    cached = domain_embeddings()

    if model is not None and cached is not None:
        names, embs = cached
        sims = util.cos_sim(model.encode(text, convert_to_tensor=True), embs)[0]
        kw = keyword_scores(text)  # explicit terms boost the semantic score
        combined = [float(sims[i]) * 100 + min(kw[n], 3) * 5 for i, n in enumerate(names)]
        i = max(range(len(names)), key=combined.__getitem__)
        conf = round(min(combined[i], 100), 1)
    else:
        kw = keyword_scores(text)
        best = max(kw, key=kw.get)
        if kw[best] == 0:
            return UNASSIGNED, 0.0
        names, i, conf = [best], 0, float(min(kw[best] * 20, 100))

    if conf < CONFIDENCE_THRESHOLD:
        return UNASSIGNED, conf
    return names[i], conf


# ============================================================
# 3. AUTH
# ============================================================
def verify_official(email, password):
    conn = get_conn()
    row = conn.execute(
        "SELECT id, name, domain, password_hash FROM officials WHERE lower(email)=?", (email.strip().lower(),)
    ).fetchone()
    conn.close()
    ok = bool(row) and check_password(password, row["password_hash"])
    log.info("Login attempt for %s: %s", email, "success" if ok else "failure")
    return row if ok else None


# ============================================================
# 4. HELPERS
# ============================================================
def esc(v):
    return html.escape(str(v if v is not None else ""), quote=True)


def safe_img(url):
    """Allow only http(s) URLs for images; otherwise None."""
    try:
        p = urlparse((url or "").strip())
        if p.scheme in ("http", "https") and p.netloc:
            return url.strip()
    except ValueError:
        pass
    return None


# ============================================================
# 5. PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Clean Hearts — Civic Triage Platform",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(THEME_CSS, unsafe_allow_html=True)
init_db()

# ============================================================
# 6. SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div class='logo-container'>
        <div class='logo-text'>🌿 CLEAN <span class='logo-leaf'>HEARTS</span></div>
        <div style='font-family: Inter; font-size: 0.75rem; letter-spacing: 3px; color: #D4C896; margin-top: 0.3rem;'>
            CIVIC TRIAGE PLATFORM
        </div>
    </div>
    """, unsafe_allow_html=True)
    page = st.radio("Navigate", ["🏠 Home", "📢 Report an Issue", "🏛️ Government Portal"],
                    label_visibility="collapsed")
    st.markdown("---")
    st.markdown("""
    <div style='font-family: Inter; font-size: 0.8rem; color: #D4C896; text-align: center; padding: 1rem;'>
        <em>"Small voices.<br>Big changes."</em>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# 7. HOME
# ============================================================
if page == "🏠 Home":
    st.markdown("<div class='subtitle'>Welcome to</div>", unsafe_allow_html=True)
    st.markdown("<div class='logo-text' style='text-align:center; font-size:3.5rem;'>🌿 CLEAN <span style='color:#6B8E23;'>HEARTS</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-quote'>Small voices. Big changes.</div>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    conn = get_conn()
    total = conn.execute("SELECT COUNT(*) FROM issues").fetchone()[0]
    sorted_count = conn.execute("SELECT COUNT(*) FROM issues WHERE status='sorted'").fetchone()[0]
    pending = conn.execute("SELECT COUNT(*) FROM issues WHERE status='pending'").fetchone()[0]
    domains = conn.execute(
        "SELECT COUNT(DISTINCT domain) FROM issues WHERE domain IS NOT NULL AND domain NOT IN ('', ?)",
        (UNASSIGNED,)).fetchone()[0] or 6
    issues = conn.execute("SELECT * FROM issues ORDER BY submitted_at DESC, id DESC LIMIT 12").fetchall()
    conn.close()

    for col, num, label in zip(st.columns(4), [total, sorted_count, pending, domains],
                               ["Total Reports", "Sorted & Routed", "Awaiting Triage", "Govt Domains"]):
        with col:
            st.markdown(f"<div class='stat-card'><span class='stat-number'>{num}</span><span class='stat-label'>{label}</span></div>", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("### 📰 Recent Civic Reports")
    st.markdown("*See how citizens are making a difference — sorted and routed to the right department.*")

    for i in range(0, len(issues), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j >= len(issues):
                continue
            it = issues[i + j]
            status, priority = it["status"] or "pending", it["priority"] or "medium"
            status_badge = f"badge-{status}" if status in ("sorted", "pending", "resolved") else "badge-pending"
            priority_badge = f"badge-{priority}" if priority in ("high", "medium", "low") else "badge-medium"
            img = esc(safe_img(it["image_url"]) or PLACEHOLDER_IMG)
            desc = it["description"]
            short = esc(desc[:140]) + ("..." if len(desc) > 140 else "")
            cat_badge = f"<span class='badge badge-domain'>{esc(it['category'])}</span>" if it["category"] else ""
            with col:
                st.markdown(f"""
                <div class='issue-card'>
                    <img class='card-image' src="{img}" alt="issue photo">
                    <div class='card-body'>
                        <div class='card-title'>{esc(it['title'])}</div>
                        <div class='card-desc'>{short}</div>
                        <div class='card-address'>📍 {esc(it['address'])}</div>
                        <div class='card-meta'>
                            <span class='badge {status_badge}'>{esc(status.upper())}</span>
                            <span class='badge {priority_badge}'>{esc(priority.upper())} PRIORITY</span>
                            {cat_badge}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ============================================================
# 8. REPORT AN ISSUE
# ============================================================
elif page == "📢 Report an Issue":
    st.markdown("## 📢 Report a Civic Issue")
    st.markdown("*Your voice matters. Describe the issue and our AI will route it to the right government department.*")
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # clear_on_submit=False so input isn't lost on validation errors
    with st.form("issue_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Issue Title *", placeholder="e.g., Overflowing garbage bin near market")
            address = st.text_input("Location / Address *", placeholder="e.g., Sector 12 Market, Delhi")
        with col2:
            image_url = st.text_input("Photo URL (optional)", placeholder="https://...")
            priority = st.selectbox("Priority Level", ["low", "medium", "high"])
        description = st.text_area("Describe the issue in detail *", height=150,
                                   placeholder="What exactly is the problem? How long has it been happening? Who is affected?")
        submitted = st.form_submit_button("🌿 Submit Report", use_container_width=True)

    if submitted:
        title, address, description = title.strip(), address.strip(), description.strip()
        image_url = image_url.strip()
        if not title or not description or not address:
            st.error("⚠️ Please fill in all required fields.")
        elif image_url and not safe_img(image_url):
            st.error("⚠️ Photo URL must start with http:// or https://")
        else:
            with st.spinner("🤖 AI is analyzing and routing your issue..."):
                domain, confidence = triage_issue(title, description)
            routed = domain != UNASSIGNED
            status = "sorted" if routed else "pending"

            conn = get_conn()
            cur = conn.execute(
                "INSERT INTO issues (title, description, address, category, image_url, status, priority, domain) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (title, description, address, domain, image_url, status, priority, domain))
            conn.commit()
            issue_id = cur.lastrowid
            conn.close()

            st.success(f"✅ Your report has been submitted! (ID: #{issue_id})")
            if routed:
                st.info(f"""
**🤖 AI Triage Result:**
- **Routed to:** `{domain}`
- **Confidence:** `{confidence}%`
- **Priority:** `{priority.upper()}`

Your issue will be reviewed by the concerned government official shortly.
""")
            else:
                st.warning(f"🤖 The AI could not confidently classify this issue (confidence {confidence}%). "
                           "It has been queued for manual review.")

# ============================================================
# 9. GOVERNMENT PORTAL
# ============================================================
elif page == "🏛️ Government Portal":
    if "official_logged_in" not in st.session_state:
        st.session_state.official_logged_in = False

    if not st.session_state.official_logged_in:
        st.markdown("## 🏛️ Government Officer Login")
        st.markdown("*Secure access for authorized government officials only.*")
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        with st.form("login_form"):
            email = st.text_input("Official Email ID", placeholder="your.name@gov.in")
            password = st.text_input("Secure Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("🔐 Authenticate", use_container_width=True)

        if submitted:
            if not email or not password:
                st.error("⚠️ Please enter both email and password.")
            else:
                result = verify_official(email, password)
                if result:
                    st.session_state.official_logged_in = True
                    st.session_state.official_id = result["id"]
                    st.session_state.official_name = result["name"]
                    st.session_state.official_domain = result["domain"]
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Access denied.")

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.info("""
**🔒 Security Notice**
- This portal is restricted to verified government officials.
- Login attempts are logged.
- Unauthorized access is a punishable offence.
""")
    else:
        domain = st.session_state.official_domain
        st.markdown(f"""
        <div class='official-header'>
            <div style='font-size: 0.85rem; letter-spacing: 2px; opacity: 0.8;'>GOVERNMENT OFFICER DASHBOARD</div>
            <div style='font-family: Playfair Display; font-size: 2rem; font-weight: 700; margin-top: 0.3rem;'>
                Welcome, {esc(st.session_state.official_name)}
            </div>
            <div style='font-family: Inter; font-size: 0.95rem; margin-top: 0.5rem;'>
                🏛️ Domain: <strong>{esc(domain)}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Logout", key="logout_btn"):
            for k in ["official_logged_in", "official_id", "official_name", "official_domain"]:
                st.session_state.pop(k, None)
            st.rerun()

        conn = get_conn()
        domain_issues = conn.execute(
            "SELECT * FROM issues WHERE domain=? ORDER BY submitted_at DESC, id DESC", (domain,)).fetchall()
        conn.close()

        STATUSES = ["pending", "sorted", "resolved"]
        counts = {s: sum(1 for i in domain_issues if i["status"] == s) for s in STATUSES}
        for col, s in zip(st.columns(3), STATUSES):
            with col:
                st.markdown(f"<div class='stat-card'><span class='stat-number'>{counts[s]}</span><span class='stat-label'>{s.title()}</span></div>", unsafe_allow_html=True)

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown(f"### 📋 Issues in `{domain}`")

        if not domain_issues:
            st.info("No issues currently assigned to your domain.")
        else:
            for it in domain_issues:
                cur_status = it["status"] if it["status"] in STATUSES else "pending"
                with st.expander(f"#{it['id']} — {it['title']} [{cur_status.upper()}]"):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.text(f"📍 Address: {it['address']}")
                        st.text(f"📝 Description: {it['description']}")
                        st.text(f"⚡ Priority: {it['priority']}")
                        st.text(f"🕒 Submitted: {it['submitted_at']}")
                    with col2:
                        img = safe_img(it["image_url"])
                        if img:
                            st.image(img, use_container_width=True)

                    st.markdown("---")
                    new_status = st.selectbox("Update Status", STATUSES, index=STATUSES.index(cur_status),
                                              key=f"status_{it['id']}")
                    notes = st.text_area("Resolution Notes", value=it["resolution_notes"] or "",
                                         key=f"notes_{it['id']}")

                    if st.button("💾 Save Changes", key=f"save_{it['id']}"):
                        conn = get_conn()
                        # Restrict updates to the official's own domain
                        conn.execute(
                            "UPDATE issues SET status=?, resolution_notes=?, sorted_by=? WHERE id=? AND domain=?",
                            (new_status, notes, st.session_state.official_name, it["id"], domain))
                        conn.commit()
                        conn.close()
                        st.rerun()
