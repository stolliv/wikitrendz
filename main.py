from data_grabber import *
import pandas
import matplotlib.pyplot as plt

data_fetcher = Data_grabber()

#trends_data = data_fetcher.get_trends_data("cat") #TODO: access to google servers is limted to one request per timeframe. Therefore: find a workaround or alternative method
#trends_data.plot()

wiki_data = data_fetcher.get_wiki_data("cat")
wiki_data.plot()

plt.show()