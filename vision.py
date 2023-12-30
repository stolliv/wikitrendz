import matplotlib.pyplot as plt
from data_grabber import Data_grabber

def plot_data(keyword):
    data_fetcher = Data_grabber()
    try:
        trends_data = data_fetcher.get_trends_data(keyword)

        wiki_data = data_fetcher.get_wiki_data(keyword, "2022-01-01T00:00:00Z", "2022-12-31T23:59:59Z")

        print("wiki_data")
        print(wiki_data)
        print("trends")
        print(trends_data)

        if trends_data.empty or wiki_data.empty:
            return -1
    except:
        return -2

    fig, ax1 = plt.subplots(figsize=(12, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Search Frequency', color=color)
    ax1.plot(trends_data.index, trends_data.iloc[:, 0], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Number of Changes', color=color)
    ax2.plot(wiki_data.index, wiki_data, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    plt.title('Google Trends for "' + keyword + '" and Wikipedia Changes for "' + keyword + '"')

    plt.tight_layout()
    plt.show()
    return True