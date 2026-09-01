-- Gambia Civic Hub — Supabase schema
-- Run this in the Supabase SQL editor to set up the shared backend.

-- Module 2: Report It
create table if not exists reports (
    id uuid primary key default gen_random_uuid(),
    category text not null,
    description text not null,
    latitude double precision not null,
    longitude double precision not null,
    region text,
    photo_url text,
    status text not null default 'Reported',
    created_at timestamptz not null default now()
);

create index if not exists idx_reports_created_at on reports (created_at desc);
create index if not exists idx_reports_status on reports (status);

-- Enable row-level security and allow public read + insert for v1 (no auth yet)
alter table reports enable row level security;

create policy "Public can read reports"
    on reports for select
    using (true);

create policy "Public can insert reports"
    on reports for insert
    with check (true);

-- Future: a `users` table + auth can be added here once you introduce login,
-- shared across all three modules (e.g. "my reports", "my saved rights topics").
