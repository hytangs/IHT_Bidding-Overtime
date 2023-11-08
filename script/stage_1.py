import pandas as pd
from datetime import datetime
import time
import copy

# Stage 1 - Standard XLSX Conversion to Recorded Auction Item Objects

# - Bidder records
generic_bidder_dict = {}
generic_bidder_id = 0


# - Datetime object => Unix timestamp
def to_timestamp(date_time):
    return time.mktime(date_time.timetuple())


# - Validation for irregular data
def validator_bids(bids, start_bid):
    bids.sort(key=lambda x: x[1], reverse=False)
    if bids[0][1] < start_bid:
        return "Data Manual Check: Start bid larger than first bid."

    _time = bids[0][2]
    for i in bids:
        if _time > i[2]:
            return "Data Manual Check: Incorrect order at " + str(i)
        _time = i[2]
    return ""


# - Main Parser
# - - Auction house standardized xlsx => Python list of auction items' basic info
def parse_auction(filename):
    # Inherit global dictionary and bidder id
    global generic_bidder_id, generic_bidder_dict

    # Create all possible token values for anonymous bidders
    anonymous_token = list(map(lambda x: str(x), range(100, 9999)))
    anonymous_token += list(map(lambda x: x + '号', anonymous_token))

    # start parsing specific auction
    print(filename)

    # read data
    data = pd.read_excel(filename, index_col=0)
    auction_data = []
    for i in data.itertuples():
        if pd.isnull(i[4]):
            continue

        # extract item demographics
        auction_house = i[0]
        auction_no = str(i[1])
        overtime_rule = i[2]
        item_index = i[3]
        item_name = i[4]
        item_start_bid = i[5]

        _full_time = datetime.strptime(str(i[6]), '%Y%m%d%H%M%S')
        item_close_time = to_timestamp(_full_time)
        _item_date = _full_time.date()
        _item_time = _full_time.time()
        item_bids = []

        # extract item bids
        _loc = 7
        _end = False

        try:
            while _end is False:
                if pd.isnull(i[_loc]):
                    _end = True
                else:
                    _bid_bidder = i[_loc]
                    # Non-unique tokens can be different bidder in multiple auctions.
                    if i[_loc] in anonymous_token:
                        _bid_bidder = str(auction_no) + "__"+ str(i[_loc])
                    if _bid_bidder in generic_bidder_dict:
                        _bidder = generic_bidder_dict[_bid_bidder]
                    else:
                        generic_bidder_dict[_bid_bidder] = generic_bidder_id
                        _bidder = generic_bidder_id
                        generic_bidder_id += 1

                    _price = i[_loc + 1]
                    _to_time = str(int(i[_loc + 2])).rjust(6, '0')
                    _bid_time = datetime.strptime(_to_time, '%H%M%S').time()
                    _timestamp = to_timestamp(datetime.combine(_item_date, _bid_time))

                    _loc += 3

                    item_bids.append([_bidder, _price, _timestamp])

        except Exception as e:
            _end = True
            if type(e) is not IndexError:
                print(e)

        _eval = validator_bids(item_bids, item_start_bid)
        if _eval != "":
            print(_eval)

        auction_data.append({"auction_house": auction_house, "auction_no": str(auction_no),
                             "overtime_rule": overtime_rule,
                             "index": item_index, "name": item_name, "start_bid": item_start_bid,
                             "close_time": item_close_time, "bids": item_bids})
    return auction_data


# - Parser for Auction House 4's special data format
# - - Auction house specific xlsx => Python list of auction items' basic info
def parse_auction_special(path, filename, tagfile):
    # Inherit global dictionary and bidder id
    global generic_bidder_id, generic_bidder_dict

    filepath = path + filename
    tagpath = path + tagfile

    # start parsing specific auction
    print(filepath)

    # extract auction no from filename
    auction_no = int(filename[:4])

    # read data and item tag
    data = pd.read_excel(filepath)
    tag = pd.read_excel(tagpath)

    item_dict = {}
    for i in tag.itertuples():
        if i[2] == auction_no:
            auction_house = i[1]
            overtime_rule = i[3]
            index = i[4]
            item_dict[index] = [auction_house,
                               overtime_rule,
                               to_timestamp(datetime.strptime(str(i[5]), '%Y%m%d%H%M%S'))]

    auction_data = []
    current = None
    bid_history = []
    item = {}
    for i in data.itertuples():
        if current != i[1]:
            current = i[1]

            # ignore unexpected item in data
            if current not in item_dict:
                continue

            # ignore unsuccessful items
            if str(i[6]) == 'nan':
                continue

            item_tag = item_dict[current]
            bid_history.reverse()
            item['bids'] = bid_history
            auction_data.append(item)
            item = {}
            bid_history = []
            item["auction_house"] = item_tag[0]
            item["auction_no"] = str(auction_no)
            item["overtime_rule"] = item_tag[1]
            item['index'] = current
            item['name'] = i[2]
            item['start_bid'] = i[5]
            item['close_time'] = item_tag[2]
            if i[4] in generic_bidder_dict:
                bidder = generic_bidder_dict[i[4]]
            else:
                bidder = generic_bidder_id
                generic_bidder_id += 1
                generic_bidder_dict[i[4]] = bidder
            bid_time = to_timestamp(datetime.strptime(str(i[6]), '%Y-%m-%d %H:%M:%S'))
            bid = [bidder, i[5], bid_time]
            bid_history.append(bid)
        else:
            if current in item_dict:
                bid_time = to_timestamp(datetime.strptime(str(i[6]), '%Y-%m-%d %H:%M:%S'))
                if i[4] in generic_bidder_dict:
                    bidder = generic_bidder_dict[i[4]]
                else:
                    bidder = generic_bidder_id
                    generic_bidder_id += 1
                    generic_bidder_dict[i[4]] = bidder
                bid = [bidder, i[5], bid_time]
                bid_history.append(bid)
    return auction_data[1:]


# recorded_object => presentable xlsx
def wide_form_export(recorded_object, hide_confidential_info):
    wide_form = []
    counter = 0
    filename = datetime.now().strftime("auction_data_%Y%m%d_%H%M%S")
    if hide_confidential_info:
        filename += "_public"
    filename += ".xlsx"

    for i in recorded_object:
        counter += 1
        auction_house = i['auction_house']
        auction_no = i['auction_no']
        overtime_rule = i['overtime_rule']
        item_index = i['index']
        close_time = i['close_time']
        bids = i['bids']
        sortedbids = copy.deepcopy(bids)
        sortedbids.sort(key=lambda x: x[1])
        if hide_confidential_info:
            auction_house = auction_no[0]
            item_index = str(counter).rjust(4, '0')
        for bid in sortedbids:
            wide_form.append([
                auction_house,
                auction_no,
                item_index,
                overtime_rule,
                datetime.fromtimestamp(close_time).strftime("%Y-%m-%d %H:%M:%S"),
                bid[0],
                bid[1],
                datetime.fromtimestamp(bid[2]).strftime("%Y-%m-%d %H:%M:%S")
            ])
    wide_form = pd.DataFrame(wide_form)
    wide_form.columns = [
        "auction_house_id",
        "auction_id",
        "item_id",
        "overtime_seconds",
        "scheduled_closing_time",
        "bidder_id",
        "bid_price",
        "bid_time",
    ]
    wide_form.to_excel("output/tables/" + filename, index=False)