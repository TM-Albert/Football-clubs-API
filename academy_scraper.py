import requests
import pandas as pd
import time
import random

# Main list to store all collected data
club_database = []

print("🚀 Starting data download and preview generation...\n")

# Loop through pages (Adjust range if the website adds more pages)
for page in range(1, 143):
    url = f"https://cert-lnp-api.laczynaspilka.pl/api/v1/searchAcademies?pageNumber={page}&pageSize=10"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            clubs = data.get('result', [])
            
            if not clubs:
                print(f"🔴 No data found on page {page}. Ending loop.")
                break

            # Temporary list for the current page (used for the console preview)
            current_page_data = []

            for club in clubs:
                # Data Mapping
                record = {
                    'details_page_id': club.get('id'),
                    'academyName': club.get('academyName'),
                    'cityName': club.get('cityName'),
                    'Certificate': club.get('starName'),    # Useful to know if Gold/Silver/Bronze
                    'FemaleTeams': 'Yes' if club.get('hasFemaleTeams') else 'No'
                }
                
                # Add to main database and temporary view list
                club_database.append(record)
                current_page_data.append(record)

            # --- ELEGANT PRINTING SECTION ---
            print(f"\n📄 PAGE {page} / 142 (Retrieved {len(current_page_data)} records)")
            # Table Header (Left aligned: <)
            print("-" * 110)
            print(f"{'ID':<6} | {'CITY':<20} | {'CERTIFICATE':<12} | {'ACADEMY NAME'}")
            print("-" * 110)
            
            # Table Rows
            for row in current_page_data:
                # Truncate city name to 19 chars and academy to 60 to prevent table misalignment
                city = (row['cityName'][:19] + '..') if len(row['cityName']) > 19 else row['cityName']
                academy = (row['academyName'][:60] + '...') if len(row['academyName']) > 60 else row['academyName']
                certificate = row['Certificate'] or "None"
                
                print(f"{row['details_page_id']:<6} | {city:<20} | {certificate:<12} | {academy}")
            
            print("-" * 110)
            # ---------------------------------------

        else:
            print(f"⚠️ Error on page {page}: Status Code {response.status_code}")
            
    except Exception as e:
        print(f"❌ Critical error on page {page}: {e}")
    
    # Random delay for safety (anti-bot protection)
    sleep_duration = random.randint(1, 5)
    time.sleep(sleep_duration)

# Summary and Save
df = pd.DataFrame(club_database)

print("\n✅ --- DOWNLOAD COMPLETE ---")
print(f"Total academies collected: {len(df)}")

# Save to CSV
filename = 'academy_database_full.csv'
df.to_csv(filename, index=False, encoding='utf-8-sig', sep=';')
print(f"📁 File '{filename}' has been saved and is ready.")