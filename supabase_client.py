"""
Shared Supabase client for all Gambia Civic Hub modules.

Requires the following in .streamlit/secrets.toml:

[supabase]
url = "https://YOUR_PROJECT.supabase.co"
key = "YOUR_ANON_OR_SERVICE_KEY"
"""

import streamlit as st
from supabase import create_client, Client


@st.cache_resource
def get_supabase_client() -> Client:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)


def insert_row(table: str, data: dict):
    """Insert a single row into a Supabase table. Returns the response."""
    client = get_supabase_client()
    return client.table(table).insert(data).execute()


def fetch_rows(table: str, filters: dict = None, order_by: str = None, desc: bool = True, limit: int = 100):
    """Fetch rows from a Supabase table with optional simple equality filters."""
    client = get_supabase_client()
    query = client.table(table).select("*")

    if filters:
        for col, val in filters.items():
            query = query.eq(col, val)

    if order_by:
        query = query.order(order_by, desc=desc)

    query = query.limit(limit)
    response = query.execute()
    return response.data
