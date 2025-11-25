import requests
import pandas as pd
import time
import random

# Lista główna na wszystkie dane
baza_klubow = []

print("🚀 Rozpoczynam pobieranie danych i generowanie podglądu...\n")

# Pętla po stronach
for page in range(1, 143):
    url = f"https://cert-lnp-api.laczynaspilka.pl/api/v1/searchAcademies?pageNumber={page}&pageSize=10"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            kluby = data.get('result', [])
            
            if not kluby:
                print(f"🔴 Brak danych na stronie {page}. Kończę działanie pętli.")
                break

            # Lista tymczasowa tylko dla tej strony (do wyświetlenia printa)
            obecna_strona_dane = []

            for club in kluby:
                # Mapowanie danych
                record = {
                    'details_page_id': club.get('id'),
                    'academyName': club.get('academyName'),
                    'cityName': club.get('cityName'),
                    'Certyfikat': club.get('starName'),     # Warto widzieć czy to Gold/Silver
                    'Druzyny Kobiece': 'Tak' if club.get('hasFemaleTeams') else 'Nie'
                }
                
                # Dodajemy do głównej bazy i do tymczasowej listy wyświetlania
                baza_klubow.append(record)
                obecna_strona_dane.append(record)

            # --- SEKCJA ELEGANCKIEGO PRINTOWANIA ---
            print(f"\n📄 STRONA {page} / 142 (Pobrano {len(obecna_strona_dane)} rekordów)")
            # Nagłówek tabeli (wyrównanie do lewej: <)
            print("-" * 110)
            print(f"{'ID':<6} | {'MIASTO':<20} | {'CERTYFIKAT':<12} | {'NAZWA AKADEMII'}")
            print("-" * 110)
            
            # Wiersze tabeli
            for row in obecna_strona_dane:
                # Skracamy nazwę miasta do 19 znaków i akademii do 50, żeby tabelka się nie rozjeżdżała
                miasto = (row['cityName'][:19] + '..') if len(row['cityName']) > 19 else row['cityName']
                akademia = (row['academyName'][:60] + '...') if len(row['academyName']) > 60 else row['academyName']
                certyfikat = row['Certyfikat'] or "Brak"
                
                print(f"{row['details_page_id']:<6} | {miasto:<20} | {certyfikat:<12} | {akademia}")
            
            print("-" * 110)
            # ---------------------------------------

        else:
            print(f"⚠️ Błąd przy stronie {page}: Kod {response.status_code}")
            
    except Exception as e:
        print(f"❌ Wystąpił błąd krytyczny na stronie {page}: {e}")
    
    ran = random.randint(1, 5)

    # Przerwa dla bezpieczeństwa
    time.sleep(ran)

# Podsumowanie i zapis
df = pd.DataFrame(baza_klubow)

print("\n✅ --- ZAKOŃCZONO POBIERANIE ---")
print(f"Łącznie zgromadzono: {len(df)} akademii.")

# Zapis do CSV
nazwa_pliku = 'baza_akademii_lnp_full.csv'
df.to_csv(nazwa_pliku, index=False, encoding='utf-8-sig', sep=';')
print(f"📁 Plik '{nazwa_pliku}' został zapisany i jest gotowy do pobrania.")