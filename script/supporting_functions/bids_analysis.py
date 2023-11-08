
# Functions that are standalone for analysis of bids in auction data

import pickle
import seaborn as sns
import matplotlib.pyplot as plt
import random


# read complete record of bids saved from auction parser
def read_all_bids():
    fileObj = open('output/object/auction_bids_dict.obj', 'rb')
    data = pickle.load(fileObj)
    fileObj.close()
    return data


# complete the bidding time-price space chart for figure 5.2
def draw_bidding_cloud(data, sampled=100):
    for rule in [60, 120, 180, 300]:
        total = range(len(data[rule]))
        included = random.sample(total, sampled)
        counter = -1
        for i in data[rule]:
            counter += 1
            if counter not in included:
                continue
            sns.set_theme()
            sns.lineplot(data=i, x='bids_time', y='bids_price', estimator='max', color='gray')
            plt.axvline(x=0, color='red', linestyle='--')
            plt.xlim(left=-100)
            plt.xlim(right=4000)
            plt.ylim(top=80000)
        item_filename = "bidding_cloud_" + str(rule) + "s.png"
        plt.savefig("output/chart/" + item_filename)
        plt.close()


# calculate the relative time and relative price for new chart
def draw_bidding_cloud_relative(data, sampled=100):
    for rule in [60, 120, 180, 300]:
        total = range(len(data[rule]))
        included = random.sample(total, sampled)
        counter = -1
        for i in data[rule]:
            counter += 1
            if counter not in included:
                continue
            i['relative_time'] = i['bids_time'] / max(i['bids_time'])
            i['relative_price'] = (i['bids_price'] - min(i['bids_price'])) / (max(i['bids_price']) - min(i['bids_price']))
            sns.set_theme()
            sns.lineplot(data=i, x='relative_time', y='relative_price', estimator='max', color='gray')
            plt.axvline(x=0, color='red', linestyle='--')
            plt.xlim(left=-1)
            plt.xlim(right=1)
            plt.ylim(top=1)
            plt.ylim(bottom=0)
        item_filename = "bidding_cloud_relative_" + str(rule) + "s.png"
        plt.savefig("output/chart/" + item_filename)
        plt.close()


