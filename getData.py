import requests
import csv
import concurrent.futures

def has_revisions_in_2022(title):
    print(f"Überprüfe Revisionen für: {title}")
    base_url = "https://en.wikipedia.org/w/api.php"
    start_date = "2000-01-01T00:00:00Z"
    end_date = "2022-12-31T23:59:59Z"
    params = {
        'action': 'query',
        'format': 'json',
        'titles': title,
        'prop': 'revisions',
        'rvlimit': 'max',
        'rvprop': 'timestamp',
        'rvstart': start_date,
        'rvend': end_date
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        pages = data['query']['pages']
        page_id = next(iter(pages))
        revisions = pages[page_id].get('revisions', [])
        result = len(revisions) > 0
        print(f"{title} hat {len(revisions)} Revision(en) im Jahr 2022.")
        return result
    else:
        print(f"Fehler beim Abrufen von Revisionen für: {title}")
        return False


def get_titles(continue_param=None):
    base_url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'allpages',
        'aplimit': 'max',
        'apfrom': 'E',  # Beginnen bei Titeln, die mit 'A' anfangen
        'apcontinue': continue_param
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['query']['allpages'], data.get('continue', {}).get('apcontinue', None)
    else:
        return [], None

def process_title(title):
    if has_revisions_in_2022(title['title']):
        return title['title']
    #print(title,": nicht ")
    return None

def save_titles_to_csv(filename, start_title=None):
    apcontinue = start_title
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        while True:
            titles, apcontinue = get_titles(apcontinue)
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                future_to_title = {executor.submit(process_title, title): title for title in titles}
                for future in concurrent.futures.as_completed(future_to_title):
                    title = future.result()
                    if title:
                        writer.writerow([title])
                        print(f"Titel gespeichert: {title}")
            if apcontinue is None:
                print("Alle Titel verarbeitet und gespeichert.")
                break

# Speichern der Titel mit mindestens einer Revision im Jahr 2022 in einer CSV-Datei
save_titles_to_csv('wiki_titles_with_2022_revisions.csv')



# import requests
# import csv
#
# def get_titles(continue_param=None):
#     base_url = "https://en.wikipedia.org/w/api.php"
#     params = {
#         'action': 'query',
#         'format': 'json',
#         'list': 'allpages',
#         'aplimit': 'max',
#         'apcontinue': continue_param
#     }
#     response = requests.get(base_url, params=params)
#     if response.status_code == 200:
#         data = response.json()
#         titles = [page['title'] for page in data['query']['allpages']]
#         apcontinue = data['continue'].get('apcontinue', None) if 'continue' in data else None
#         return titles, apcontinue
#     else:
#         return [], None
#
# def save_titles_to_csv(filename, start_title=None):
#     apcontinue = start_title
#     with open(filename, mode='a', newline='', encoding='utf-8') as file:  # Mode 'a' zum Anhängen
#         writer = csv.writer(file)
#         while True:
#             titles, apcontinue = get_titles(apcontinue)
#             for title in titles:
#                 writer.writerow([title])
#             if apcontinue is None:
#                 break
#
# save_titles_to_csv('wiki_titles.csv', start_title='Roger Bailey')
