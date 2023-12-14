from pytrends.request import TrendReq
import pandas as pd
import requests

class Data_grabber:
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.wiki_data = None

    def get_trends_data(self, keyword: str): # TODO: Add timeframe as parameter
        keyword_list = [keyword]
        self.pytrends.build_payload(keyword_list, cat=0, timeframe="2022-01-01 2022-12-31", geo='', gprop='')
        interest_over_time = self.pytrends.interest_over_time()
        return interest_over_time

    def get_wiki_data(self, keyword: str, start_date: str, end_date: str, exclude_user: str = None):
        session = requests.Session()
        url = "https://en.wikipedia.org/w/api.php"

        params = {
            "action": "query",
            "prop": "revisions",
            "titles": keyword,
            "rvlimit": "max",
            "rvprop": "timestamp|user|comment",
            "rvdir": "newer",
            "rvstart": start_date,
            "rvend": end_date,
            "formatversion": "2",
            "format": "json"
        }

        if exclude_user:
            params["rvexcludeuser"] = exclude_user

        response = session.get(url=url, params=params)
        data = response.json()

        # Verarbeiten der Daten
        changes = []
        for page in data["query"]["pages"]:
            for revision in page.get("revisions", []):
                changes.append(revision['timestamp'])

        df = pd.DataFrame(changes, columns=['timestamp'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)

        # Gruppieren und Zählen der Änderungen pro Zeitintervall (z.B. pro Tag)
        grouped_data = df.resample('D').size()
        return grouped_data
