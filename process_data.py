"""
Auction Data Processor
"""

from script import stage_1, stage_2
import os
import pandas as pd


# Stage 1 - Raw XLSX Conversion to Recorded Auction Item Objects
# (auction house data) => recorded_object
def stage_1_main():
    recorded_object = []
    path = "data/standard/"
    dir_list = os.listdir(path)
    dir_list.sort()

    # get file location and process files
    files = list(map(lambda x: path + x, dir_list))
    for i in files:
        try:
            if i[-5:] != '.xlsx':
                continue
            records = stage_1.parse_auction(i)
            recorded_object = recorded_object + records
        except Exception as e:
            print(e)

    sp_path = "data/special/"
    sp_tag = "tag.xlsx"
    sp_list = os.listdir(sp_path)
    sp_list.sort()

    for i in sp_list:
        if i != sp_tag:
            try:
                if i[-5:] != '.xlsx':
                    continue
                records = stage_1.parse_auction_special(path=sp_path, filename=i, tagfile=sp_tag)
                recorded_object = recorded_object + records
            except Exception as e:
                print(e)

    return recorded_object


# recorded_object => presentable xlsx
def stage_1_export(recorded_object, hide_confidential_info=False):
    stage_1.wide_form_export(recorded_object, hide_confidential_info)


# Stage 2 - Recorded Auction Item Objects to Inferred Auction Item Objects
# recorded_object => inferred_object
def stage_2_main(recorded_object):
    data = pd.DataFrame(recorded_object)
    inferred = stage_2.process_inferred(data)
    inferred_object = pd.concat([data, inferred], axis=1)
    return inferred_object


# inferred_object => file_storage & presentable xlsx
def stage_2_savefile(inferred_object):
    stage_2.save_auctions(inferred_object)
    stage_2.export_auctions(inferred_object)


# file_storage => inferred_object
def stage_2_readfile():
    return stage_2.read_auctions()


# main script
print("\nStage 1\n")
recorded_object = stage_1_main()

print("\nExport file - Confidential")
stage_1_export(recorded_object, hide_confidential_info=False)

print("\nExport file - Public")
stage_1_export(recorded_object, hide_confidential_info=True)

print("\nStage 2\n")
inferred_object = stage_2_main(recorded_object)

print("\nBidding Charts Generated\n")
stage_2_savefile(inferred_object)
