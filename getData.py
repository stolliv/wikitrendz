import requests
import csv

def get_titles(continue_param=None):
    base_url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'allpages',
        'aplimit': 'max',
        'apcontinue': continue_param
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        titles = [page['title'] for page in data['query']['allpages']]
        apcontinue = data['continue'].get('apcontinue', None) if 'continue' in data else None
        return titles, apcontinue
    else:
        return [], None

def save_titles_to_csv(filename, start_title=None):
    apcontinue = start_title
    with open(filename, mode='a', newline='', encoding='utf-8') as file:  # Mode 'a' zum Anhängen
        writer = csv.writer(file)
        while True:
            titles, apcontinue = get_titles(apcontinue)
            for title in titles:
                writer.writerow([title])
            if apcontinue is None:
                break

# Fortsetzen des Speicherns der Titel in der CSV-Datei
save_titles_to_csv('wikipedia_titles.csv', start_title='Toxicity (System of a Down Single)')
