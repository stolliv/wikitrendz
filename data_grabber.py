from pytrends.request import TrendReq
import pandas as pd
import requests

class Data_grabber:
    def __init__(self):
        #self.pytrends = TrendReq(hl='en-US', tz=360)
        pass

    def get_trends_data(self, keyword: str): # TODO: Add timeframe as parameter
        keyword_list = [keyword]
        self.pytrends.build_payload(keyword_list, cat=0, timeframe='today 5-y', geo='', gprop='')
        interest_over_time = self.pytrends.interest_over_time()
        return interest_over_time

    def get_wiki_data(self, keyword:str):
        session = requests.Session()
        request_url = "https://en.wikipedia.org/w/api.php"
        parameters = {
            "action": "query",
            "prop": "revisions",
            "titles": keyword,
            "rvprop": "timestamp",#"timestamp|user|comment|content"
            "rvlimit": "500", # TODO: rvlimit is sadly mandatory meaning the rvstart and rvend parameters will only work as expected when the result amount for said timeframe is within this limit, i.e. <= 500.  To resolve maybe split into smaller segments
            #"rvstart": "2022-01-15T14:56:00Z",
            #"rvend": "2020-01-15T14:56:00Z",  
            "formatversion": "2",
            "format": "json"
        }

        request = session.get(url=request_url, params=parameters)
        data = request.json()

        pages = data["query"]["pages"]
        revision_times = [page["revisions"] for page in pages][0]

        revision_df = pd.DataFrame.from_records(revision_times)
        revision_df["timestamp"] = pd.to_datetime(revision_df["timestamp"])
        revision_df.set_index('timestamp', inplace=True)
        revisions_per_day_df = revision_df.resample('D').size()

        return revisions_per_day_df
