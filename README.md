# 🇬🇲 Gambia Civic Hub

One platform, three civic-tech modules:

1. **⚖️ Know Your Rights & Civic Literacy** — RAG-grounded chatbot on constitutional rights, how government works, and elections. Reuses the pattern from your existing Know Your Rights Gambia project.
2. **📍 Report It** — Citizens report local issues (roads, water, waste) with photo + location; shown on a public map.
3. **💰 Budget Tracker** — Dashboard + chatbot over digitized government budget data.

## Project structure
```
gambia_civic_hub/
├── app.py                     # Main entrypoint + navigation
├── modules/
│   ├── rights_civic.py        # Module 1
│   ├── report_it.py           # Module 2
│   └── budget_tracker.py      # Module 3
├── utils/
│   ├── supabase_client.py     # Shared Supabase helpers
│   └── gemini_client.py       # Shared Gemini helpers
├── data/
│   └── sample_budget.csv      # Placeholder budget data — replace with real digitized figures
├── supabase_schema.sql        # Run this in Supabase SQL editor
└── .streamlit/secrets.toml.example
```

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Supabase**
   - Create a project at supabase.com
   - Run `supabase_schema.sql` in the SQL editor to create the `reports` table
   - (Optional) Create a Storage bucket named `report-photos` for photo uploads

3. **Configure secrets**
   - Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`
   - Fill in your Supabase URL/key and Gemini API key

4. **Run it**
   ```bash
   streamlit run app.py
   ```

## What's stubbed vs. what's real

- ✅ Navigation shell, module structure, Supabase schema, and UI are functional
- ⚠️ **Module 1** currently calls Gemini directly without RAG retrieval — hook in your existing Chroma vector store (from Know Your Rights Gambia) where marked `TODO` in `rights_civic.py`
- ⚠️ **Module 2** photo upload is stubbed — wire up Supabase Storage upload where marked `TODO` in `report_it.py`
- ⚠️ **Module 3** ships with 6 rows of **placeholder/fictional** budget figures in `sample_budget.csv` — replace with real digitized data from official Ministry of Finance budget documents before using for anything real

## Next steps (suggested order)
1. Wire Module 1's RAG store in (fastest win — you already have this built)
2. Wire up Supabase Storage for report photos in Module 2
3. Start digitizing one real sector/year of budget data for Module 3
