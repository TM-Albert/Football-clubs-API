# ⚽ Polish Football Academy Scraper & Enricher

A powerful, two-stage data extraction pipeline designed to build a comprehensive database of certified Polish football academies.

This tool automates the process of gathering official academy data from the PZPN (Polish Football Association) "Łączy Nas Piłka" portal and enriches it with external website links using Google Search technology.

## 🚀 Features

* **Smart API Scraping:** Iterates through the official certification API to retrieve granular details (Academy Name, City, Certification Level, Female Team status).
* **Live Console Dashboard:** Displays a neatly formatted table in the terminal as data is being fetched.
* **Data Enrichment:** Uses the Serper API to perform Google searches for every academy, finding their official websites or social media profiles.
* **Fault Tolerance:** Includes auto-save functionality and "resume" logic. If the script crashes or is stopped, it picks up exactly where it left off.
* **Anti-Bot Handling:** Implements randomized delays to mimic human behavior and prevent IP blocking.

## 🛠️ Prerequisites

* Python 3.x
* A free **Serper API Key** (for the enrichment step).

### Libraries

Install the required Python packages:

```bash
pip install requests pandas
```

## 🔑 Serper API Setup

* Visit https://serper.dev and create a free account.
* After email verification, you receive 2,500 free queries.
* Copy your personal API Key.
* Insert it into data_enricher.py:

```bash
API_KEY = "your_key_goes_here"
```

## 📖 Usage Guide

### Step 1 — Scrape Academy Data

Runs queries against the PZPN certification API and builds the base dataset:
```bash
python academy_scraper.py
```

Output file:
```bash
academy_database_full.csv
```


### Step 2 — Enrich with Websites & Links

Performs automated Google search queries to find official URLs:
```bash
python website_links_enricher.py
```

Output file:
```bash
academy_database_enriched.csv
```

This file includes:
* All scraped fields
* A new column with top-matched website URLs


## 📂 Project Structure

| File                            | Description                                                                 |
|-------------------------------- |---------------------------------------------------------------------------- |
| `academy_scraper.py`            | Downloads all academy data from the certification API.                      |
| `website_links_enricher.py`     | Enriches scraped CSV by querying Serper API and appending URLs.             |
| `academy_database_full.csv`     | Raw scraped data (Step 1).                                                  |
| `academy_database_enriched.csv` | Final enriched dataset (Step 2).                                            |