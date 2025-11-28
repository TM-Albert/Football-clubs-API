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