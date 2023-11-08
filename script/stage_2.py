import pandas as pd
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
from script.supporting_functions import item_classifier


# Stage 2 - Recorded Auction Item Objects to Inferred Auction Item Objects

# - Iterate by row and call row processing function
def process_inferred(all_data):
    all_inferred = []
    bids_all = {}
    for row in all_data.itertuples():
        inferred, bids_all = process_inferred_by_row(row, bids_all)
        all_inferred.append(inferred)

    export_all_bids(bids_all)
    all_inferred = pd.DataFrame(all_inferred)
    all_inferred.columns = [
        "item_type",
        "winner",
        "winning_bid",
        "winning_time",
        "total_bids",
        "overtime_length",
        "bid_before_close",
        "time_to_close",
        "normal_bids",
        "overtime_bids",
        "is_winner_overtime",
        "is_overtime_item",
        "list_bidders",
        "list_overtime_new_bidders",
        "count_bidders",
        "count_overtime_bidders",
    ]
    return pd.DataFrame(all_inferred)


# - Row processing and add inferred parameters for each auction record
def process_inferred_by_row(row, _df_all=None):
    if _df_all is None:
        _df_all = {}
    inferred = []

    # extracted basic data
    overtime_rule = row[3]
    item_name = row[5]
    start_price = row[6]
    closing_timestamp = row[7]
    bids = row[8]

    # eval item type
    item_type = item_classifier.item_classifier(item_name)
    inferred.append(item_type)

    # sort bids from highest to lowest
    bids.sort(key=lambda x: x[1], reverse=True)

    # winner details
    winning_bidder = bids[0][0]
    inferred.append(winning_bidder)
    winning_price = bids[0][1]
    inferred.append(winning_price)
    winning_timestamp = bids[0][2]
    inferred.append(winning_timestamp)

    # total bids
    total_bids = len(bids)
    inferred.append(total_bids)

    # bid durations
    overtime_length = winning_timestamp - closing_timestamp
    inferred.append(overtime_length)

    # bidder demographics and bid history
    # active bidding definition: two bids placed within 3 minutes interval (180 seconds)
    bids.sort(key=lambda x: x[1], reverse=False)

    _list_bidders = set()
    _counter_normal_bids = 0
    _list_overtime_bidders = set()
    _pointer = False
    _active = False
    _last_bid = start_price
    _last_time = closing_timestamp

    time_to_close = -1
    bid_before_close = start_price

    for i in bids:
        if _pointer is False:
            if i[2] > closing_timestamp:
                _pointer = True
                bid_before_close = _last_bid
                time_to_close = closing_timestamp - _last_time
                if i[0] not in _list_bidders and i[0] not in _list_overtime_bidders:
                    _list_overtime_bidders.add(i[0])
            else:
                _counter_normal_bids += 1
                _last_time = i[2]
                _last_bid = i[1]
                if i[0] not in _list_bidders:
                    _list_bidders.add(i[0])
        elif i[0] not in _list_bidders and i[0] not in _list_overtime_bidders:
            _list_overtime_bidders.add(i[0])

    inferred.append(bid_before_close)
    inferred.append(time_to_close)

    # Normal and overtime bids
    normal_bids = _counter_normal_bids
    overtime_bids = total_bids - normal_bids
    inferred.append(normal_bids)
    inferred.append(overtime_bids)

    # check if winning bidder enters in overtime
    if winning_bidder in _list_overtime_bidders:
        inferred.append(True)
    else:
        inferred.append(False)

    if overtime_length > 0:
        inferred.append(True)
    else:
        inferred.append(False)

    inferred.append(_list_bidders)
    inferred.append(_list_overtime_bidders)
    inferred.append(len(_list_bidders))
    inferred.append(len(_list_overtime_bidders))

    # draw bids in chart
    bids_time = []
    bids_price = []
    bids_bidder = []
    for i in bids:
        bids_price.append(i[1])
        bids_time.append(i[2])
        bids_bidder.append(i[0])
    bids_time = list(map(lambda x: x - closing_timestamp, bids_time))

    _df = pd.DataFrame({'bids_time': bids_time, 'bids_price': bids_price, 'bidder': bids_bidder})

    if overtime_rule in _df_all:
        _df_all[overtime_rule].append(_df)
    else:
        _df_all[overtime_rule] = [_df, ]

    # check for active bidding period
    return inferred, _df_all


# save auctions into objects
def save_auctions(data):
    fileObj = open('output/object/auction_data_full.obj', 'wb')
    pickle.dump(data, fileObj)
    fileObj.close()
    print("current version saved to file")


# read auctions from objects
def read_auctions():
    fileObj = open('output/object/auction_data_full.obj', 'rb')
    data = pickle.load(fileObj)
    fileObj.close()
    return data


# export auctions into presentable xlsx
def export_auctions(data):
    filename = datetime.now().strftime("auction_data_inferred_%Y%m%d_%H%M%S")
    filename += ".xlsx"
    data.to_excel("output/tables/" + filename, index=False)


# export all bids sequence into object
def export_all_bids(bids):
    fileObj = open('output/object/auction_bids_dict.obj', 'wb')
    pickle.dump(bids, fileObj)
    fileObj.close()
    print("current version saved to file")