import streamlit as st

st.set_page_config(
    page_title="Gambia Civic Hub",
    page_icon="🇬🇲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Global styles ----------
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #CE1126;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1rem;
        color: #666;
        margin-top: 0;
    }
    .module-card {
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid #eee;
        background: #fafafa;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar navigation ----------
st.sidebar.markdown("## 🇬🇲 Gambia Civic Hub")
st.sidebar.caption("Know your rights. Report issues. Track the budget.")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "⚖️ Know Your Rights & Civic Literacy",
        "📍 Report It",
        "💰 Budget Tracker",
    ],
    label_visibility="collapsed",
)

st.sidebar.divider()
st.sidebar.caption("Built for The Gambia 🇬🇲 · v0.1 (in development)")

# ---------- Routing ----------
if page == "🏠 Home":
    st.markdown('<p class="main-header">Gambia Civic Hub</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">One platform to understand your rights, report local issues, and track how public money is spent.</p>', unsafe_allow_html=True)
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.subheader("⚖️ Know Your Rights")
        st.write("Ask questions about your constitutional rights, how government works, and how elections are run — in plain language.")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.subheader("📍 Report It")
        st.write("Report broken roads, water shortages, waste, or other local issues with a photo and location. See what's been reported near you.")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.subheader("💰 Budget Tracker")
        st.write("Explore how the national budget is allocated and spent, sector by sector, in numbers anyone can understand.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.info("Use the sidebar to open a module. This is an early build — modules will fill in as they're developed.")

elif page == "⚖️ Know Your Rights & Civic Literacy":
    from modules import rights_civic
    rights_civic.render()

elif page == "📍 Report It":
    from modules import report_it
    report_it.render()

elif page == "💰 Budget Tracker":
    from modules import budget_tracker
    budget_tracker.render()
