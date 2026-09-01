"""
Module 1: Know Your Rights & Civic Literacy

Merges the existing "Know Your Rights Gambia" RAG chatbot with civic/election
literacy content. Reuses the RAG pattern from your existing project — swap in
your Chroma vector store connection where marked below.
"""

import streamlit as st
from utils.gemini_client import start_chat_session

SYSTEM_INSTRUCTION = """You are a civic education assistant for citizens of The Gambia.
You answer questions about:
- Constitutional rights and freedoms
- How the three branches of government work
- How elections and voter registration work in The Gambia
- Civic responsibilities

Rules:
- Answer in plain, simple language — assume no legal background.
- Ground answers in the Gambian Constitution and IEC (electoral commission) processes where relevant.
- If unsure or the question falls outside Gambian civic/legal content, say so clearly rather than guessing.
- Always include a short disclaimer that this is general information, not legal advice.
- Keep answers concise unless the user asks for more detail.
"""

CATEGORIES = [
    "Constitutional Rights",
    "Freedom of Expression",
    "Voting & Elections",
    "Local Government",
    "Justice System",
    "Labor Rights",
    "Land Rights",
    "Women's & Children's Rights",
    "Education Rights",
    "Healthcare Rights",
    "Civic Responsibilities",
]


def render():
    st.header("⚖️ Know Your Rights & Civic Literacy")
    st.caption("Ask about your rights, how government works, or how elections work in The Gambia.")

    with st.expander("Browse by category"):
        cols = st.columns(3)
        for i, cat in enumerate(CATEGORIES):
            if cols[i % 3].button(cat, use_container_width=True):
                st.session_state.rights_prefill = f"Tell me about {cat.lower()} in The Gambia."

    if "rights_chat" not in st.session_state:
        st.session_state.rights_chat = start_chat_session(system_instruction=SYSTEM_INSTRUCTION)
        st.session_state.rights_messages = []

    # Render history
    for msg in st.session_state.rights_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prefill = st.session_state.pop("rights_prefill", None)
    user_input = st.chat_input("Ask about your rights or how government/elections work...")
    query = prefill or user_input

    if query:
        st.session_state.rights_messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # TODO: Insert RAG retrieval step here before calling Gemini —
                # retrieve relevant chunks from your Chroma store (reuse Cheat Mind's
                # RAG pattern) and prepend them to `query` as context.
                response = st.session_state.rights_chat.send_message(query)
                st.markdown(response.text)

        st.session_state.rights_messages.append({"role": "assistant", "content": response.text})

    st.divider()
    st.caption("⚠️ This tool provides general civic information, not legal advice. For specific legal matters, consult a qualified lawyer or the relevant government office.")
