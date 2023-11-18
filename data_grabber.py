from pytrends.request import TrendReq
import pandas as pd
import requests

class Data_grabber:
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.wiki_data = None

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
            "rvslots": "main",
            "formatversion": "2",
            "format": "json"
        }

        request = session.get(url=request_url, params=parameters)
        data = request.json()
        pages = data["query"]["pages"] # TODO: Currently only one revision is returned, fix this
