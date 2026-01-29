import http.client
import json
import pandas as pd
import time
import random
import sys

# --- CONFIGURATION ---
# Sign up at https://serper.dev to get your free API key (2,500 credits)
API_KEY = ""        # <--- PASTE YOUR KEY HERE
INPUT_FILE = 'academy_database_full.csv'     # <--- Ensure this matches the output of the scraper
OUTPUT_FILE = 'academy_database_enriched.csv'    # <--- Final file with links

# Check if API key is set
if not API_KEY or API_KEY == "YOUR_SERPER_API_KEY_HERE":
    print("ERROR: You must paste your Serper API Key in the script before running!")
    sys.exit()

def get_google_links(query):
    """
    Function to query Serper API using http.client and return top 5 organic links.
    """
    conn = http.client.HTTPSConnection("google.serper.dev")
    
    payload = json.dumps({
        "q": query,
        "location": "Poland",
        "gl": "pl",
        "hl": "pl"
    })
    
    headers = {
        'X-API-KEY': API_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        conn.request("POST", "/search", payload, headers)
        res = conn.getresponse()
        data = res.read()
        
        # Decode and Parse JSON
        response_json = json.loads(data.decode("utf-8"))
        
        # Extract top 5 organic links
        organic_results = response_json.get('organic', [])
        top_links = []
        
        for result in organic_results[:5]:
            if 'link' in result:
                top_links.append(result['link'])
                
        # Join links with a pipe delimiter for the CSV column
        return " ".join(top_links)

    except Exception as e:
        print(f"API Request Error: {e}")
        return None
    finally:
        conn.close()

# --- MAIN EXECUTION ---

print("Starting the Serper enrichment process...")

# 1. Load Data
try:
    # Logic to resume work: Try loading the output file first
    try:
        df = pd.read_csv(OUTPUT_FILE, sep=';')
        print(f"Found existing output file '{OUTPUT_FILE}'. Resuming process...")
    except FileNotFoundError:
        # If output doesn't exist, load the original input
        try:
            df = pd.read_csv(INPUT_FILE, sep=';')
            print(f"Loaded input file '{INPUT_FILE}'.")
        except FileNotFoundError:
            print(f"CRITICAL: Input file '{INPUT_FILE}' not found. Run the scraper first!")
            sys.exit()

    # Create 'Links' column if it doesn't exist
    if 'Links' not in df.columns:
        df['Links'] = None

    total_records = len(df)
    processed_count = 0

    print(f"Total records to process: {total_records}")
    print("-" * 60)

    # 2. Iterate through records
    for index, row in df.iterrows():
        
        # Skip if links are already scraped (resume logic)
        if pd.notna(row['Links']) and row['Links'] != "":
            continue

        academy_name = row['academyName']
        city = row['cityName'] # Adding city to the query ensures better accuracy
        search_query = f"{academy_name} {city}"
        
        print(f"[{index + 1}/{total_records}] Searching for: '{search_query}'...")

        # Call the API
        links_found = get_google_links(search_query)

        if links_found:
            df.at[index, 'Links'] = links_found
            print(f"Found links.")
        else:
            print(f"No links found or API error.")

        processed_count += 1

        # 3. Save periodically (Every 10 records) to prevent data loss
        if processed_count % 10 == 0:
            df.to_csv(OUTPUT_FILE, index=False, sep=';', encoding='utf-8-sig')
            print(f"[Auto-Save] Progress saved to '{OUTPUT_FILE}'")

        # 4. Random Delay (1-6 seconds) to be polite to the API
        sleep_time = random.uniform(1, 6)
        time.sleep(sleep_time)

except KeyboardInterrupt:
    print("\n\nProcess interrupted by user!")

except Exception as e:
    print(f"\n\nCRITICAL ERROR: {e}")

finally:
    # 5. Final Save on Exit/Crash
    print("-" * 60)
    print("Saving final data before exiting...")
    if 'df' in locals():
        df.to_csv(OUTPUT_FILE, index=False, sep=';', encoding='utf-8-sig')
        print(f"Data successfully saved to '{OUTPUT_FILE}'.")
    else:
        print("⚠️ DataFrame was not created, nothing to save.")
    
    print("👋 Process finished.")
