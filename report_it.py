"""
Module 2: Report It

Citizens report local issues (roads, water, waste, etc.) with a photo,
location, and description. Reports are stored in Supabase and shown on a
public map + list.
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import datetime

from utils.supabase_client import insert_row, fetch_rows

CATEGORIES = ["Road", "Water", "Waste/Sanitation", "Electricity", "Public Safety", "Other"]
STATUSES = ["Reported", "Acknowledged", "In Progress", "Resolved"]

# Rough center of The Gambia (near Banjul) for default map view
DEFAULT_LAT, DEFAULT_LON = 13.4549, -16.5790


def render():
    st.header("📍 Report It")
    st.caption("Report a local issue, or see what's been reported near you.")

    tab_report, tab_map, tab_list = st.tabs(["🆕 Report an Issue", "🗺️ Map View", "📋 All Reports"])

    # ---------------- Report an Issue ----------------
    with tab_report:
        with st.form("report_form", clear_on_submit=True):
            category = st.selectbox("Category", CATEGORIES)
            description = st.text_area("Describe the issue", placeholder="e.g. Large pothole blocking half the road near...")
            photo = st.file_uploader("Photo (optional but recommended)", type=["jpg", "jpeg", "png"])

            col1, col2 = st.columns(2)
            with col1:
                lat = st.number_input("Latitude", value=DEFAULT_LAT, format="%.6f")
            with col2:
                lon = st.number_input("Longitude", value=DEFAULT_LON, format="%.6f")
            st.caption("Tip: use your phone's GPS/maps app to find your coordinates, or drop a pin on the Map View tab in a future version.")

            region = st.text_input("Region / Area name", placeholder="e.g. Serrekunda, Kanifing, Brikama")
            submitted = st.form_submit_button("Submit Report", use_container_width=True)

            if submitted:
                if not description:
                    st.error("Please describe the issue before submitting.")
                else:
                    photo_url = None
                    # TODO: upload `photo` to Supabase Storage bucket and set photo_url
                    # e.g. supabase.storage.from_("report-photos").upload(...)

                    insert_row("reports", {
                        "category": category,
                        "description": description,
                        "latitude": lat,
                        "longitude": lon,
                        "region": region,
                        "photo_url": photo_url,
                        "status": "Reported",
                        "created_at": datetime.utcnow().isoformat(),
                    })
                    st.success("Report submitted. Thank you for helping improve your community!")

    # ---------------- Map View ----------------
    with tab_map:
        try:
            reports = fetch_rows("reports", order_by="created_at")
        except Exception as e:
            reports = []
            st.warning(f"Couldn't load reports yet — check your Supabase connection. ({e})")

        m = folium.Map(location=[DEFAULT_LAT, DEFAULT_LON], zoom_start=11)
        for r in reports:
            popup = f"<b>{r.get('category', 'Issue')}</b><br>{r.get('description', '')}<br><i>{r.get('status', 'Reported')}</i>"
            folium.Marker(
                location=[r["latitude"], r["longitude"]],
                popup=popup,
                icon=folium.Icon(color="red" if r.get("status") == "Reported" else "green"),
            ).add_to(m)

        st_folium(m, use_container_width=True, height=500)

    # ---------------- All Reports (list) ----------------
    with tab_list:
        try:
            reports = fetch_rows("reports", order_by="created_at")
        except Exception as e:
            reports = []
            st.warning(f"Couldn't load reports yet — check your Supabase connection. ({e})")

        if not reports:
            st.info("No reports yet. Be the first to report an issue!")
        else:
            for r in reports:
                with st.container(border=True):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"**{r.get('category', 'Issue')}** — {r.get('region', 'Unknown area')}")
                        st.write(r.get("description", ""))
                    with col2:
                        st.markdown(f"`{r.get('status', 'Reported')}`")
