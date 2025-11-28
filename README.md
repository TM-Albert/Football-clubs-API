# Football-clubs-API
Football clubs API contains script to download all football clubs in Poland that are listed in official laczynaspilka.pl website

⚽ Polish Football Academy Scraper & Enricher

A powerful, two-stage data extraction pipeline designed to build a comprehensive database of certified Polish football academies.

This tool automates the process of gathering official academy data from the PZPN (Polish Football Association) "Łączy Nas Piłka" portal and enriches it with external website links using Google Search technology.

🚀 Features

Smart API Scraping: Iterates through the official certification API to retrieve granular details (Academy Name, City, Certification Level, Female Team status).

Live Console Dashboard: Displays a neatly formatted table in the terminal as data is being fetched.

Data Enrichment: Uses the Serper API to perform Google searches for every academy, finding their official websites or social media profiles.

Fault Tolerance: Includes auto-save functionality and "resume" logic. If the script crashes or is stopped, it picks up exactly where it left off.

Anti-Bot Handling: Implements randomized delays to mimic human behavior and prevent IP blocking.

🛠️ Prerequisites

Python 3.x

A free Serper API Key (for the enrichment step).

Libraries

Install the required Python packages:

pip install requests pandas


🔑 Serper API Setup (Free)

This project uses Serper.dev for Google Search results. It is the fastest and cheapest Google Search API available.

Go to Serper.dev and sign up.

You will receive 2,500 free queries immediately upon email verification.

Copy your API Key from the dashboard.

Paste it into the data_enricher.py file:

API_KEY = "your_key_goes_here"


📖 Usage Guide

Step 1: Gather the Data

Run the scraper to build the base dataset. This communicates with the Łączy Nas Piłka API.

python academy_scraper.py


Output: A file named academy_database_full.csv.

Step 2: Enrich with Web Links

Run the enricher to find websites for the academies found in Step 1.

python data_enricher.py


Output: A file named academy_database_enriched.csv containing the original data plus a new column with top Google results.

📂 Project Structure

File

Description

academy_scraper.py

Connects to the certification API, iterates through pages, and saves basic academy info.

data_enricher.py

Reads the scraped CSV, queries Google via Serper API, and appends URLs.

academy_database_full.csv

Raw output from Step 1.

academy_database_enriched.csv

Final output from Step 2 (includes websites).
