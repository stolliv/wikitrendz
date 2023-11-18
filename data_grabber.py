from pytrends.request import TrendReq
import pandas

class Data_grabber:
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.wiki_data = None

    def get_trends_data(self, keyword: str): # TODO: Add timeframe as parameter
        keyword_list = [keyword]
        self.pytrends.build_payload(keyword_list, cat=0, timeframe='today 5-y', geo='', gprop='')
        interest_over_time = self.pytrends.interest_over_time()
        return interest_over_time

    def get_wiki_data(self):
        pass