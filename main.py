from data_grabber import *
import pandas
import matplotlib.pyplot as plt

data_fetcher = Data_grabber()
data = data_fetcher.get_trends_data("cats")
data.plot()


plt.show()