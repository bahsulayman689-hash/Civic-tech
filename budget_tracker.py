"""
Module 3: Budget Tracker

Dashboard + chatbot over digitized national/local government budget data.
Starts with a single manually-digitized sector/year and grows from there —
see /data/sample_budget.csv for the expected schema.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import os

from utils.gemini_client import ask_gemini

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sample_budget.csv")

SYSTEM_INSTRUCTION = """You are a budget transparency assistant for citizens of The Gambia.
You explain government budget allocations and spending in plain, non-technical language.
Only answer based on the budget data provided to you in the prompt — if the data doesn't
cover something, say so rather than guessing figures.
"""


@st.cache_data
def load_budget_data():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    return pd.DataFrame(columns=["year", "sector", "allocated_gmd", "spent_gmd"])


def render():
    st.header("💰 Budget Tracker")
    st.caption("See how the national budget is allocated and spent, sector by sector.")

    df = load_budget_data()

    if df.empty:
        st.info(
            "No budget data loaded yet. Add digitized figures to "
            "`data/sample_budget.csv` with columns: year, sector, allocated_gmd, spent_gmd."
        )
        st.code("year,sector,allocated_gmd,spent_gmd\n2024,Education,1200000000,1100000000\n2024,Health,950000000,880000000", language="csv")
        return

    years = sorted(df["year"].unique())
    selected_year = st.selectbox("Year", years, index=len(years) - 1)
    year_df = df[df["year"] == selected_year]

    col1, col2 = st.columns([2, 1])

    with col1:
        fig = px.bar(
            year_df.sort_values("allocated_gmd", ascending=False),
            x="sector", y=["allocated_gmd", "spent_gmd"],
            barmode="group",
            labels={"value": "GMD", "sector": "Sector", "variable": "Type"},
            title=f"Budget Allocated vs Spent by Sector ({selected_year})",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        total_allocated = year_df["allocated_gmd"].sum()
        total_spent = year_df["spent_gmd"].sum()
        st.metric("Total Allocated", f"D{total_allocated:,.0f}")
        st.metric("Total Spent", f"D{total_spent:,.0f}")
        utilization = (total_spent / total_allocated * 100) if total_allocated else 0
        st.metric("Utilization", f"{utilization:.1f}%")

    st.dataframe(year_df, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Ask about the budget")
    question = st.chat_input("e.g. How much was spent on Education in 2024?")
    if question:
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            with st.spinner("Checking the numbers..."):
                context = year_df.to_csv(index=False)
                prompt = f"Budget data for {selected_year} (GMD):\n{context}\n\nQuestion: {question}"
                answer = ask_gemini(prompt, system_instruction=SYSTEM_INSTRUCTION)
                st.markdown(answer)

    st.caption("⚠️ Figures are manually digitized from public budget documents and may contain errors. Always cross-check with official Ministry of Finance publications.")
