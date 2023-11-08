
"""
Auction Data Analyzer for Cleaned and Standardised Auction Data
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import numpy as np


# Function to calculate bidding intervals and make lists of (time-normalized, interval)
def calculate_intervals(normalized_time):
    intervals = []
    for i in range(1, len(normalized_time)):
        interval = normalized_time[i] - normalized_time[i - 1]
        intervals.append((normalized_time[i], interval))
    return intervals


# Function to find the start of the active bidding stage
def find_active_start(intervals, threshold=900):
    start_time = None

    for time, interval in intervals:
        if interval <= threshold:
            if start_time is None:
                start_time = time
        else:
            start_time = None

    return start_time


# Plot and save the price growth path with a vertical line at the start of the active bidding stage
def plot_price_growth(data, output_filename):
    sns.set()
    plt.figure(figsize=(8, 5))

    bids = data['bids']
    normalized_time = data['normalized_time']
    bidders = data['bidders']
    intervals = data['intervals']

    # Assign different shapes for early and active bids
    markers = ['o' if (time is not None and time <= data['active_start']) else 's' for time in normalized_time]

    # Different colors for each bidder
    unique_bidders = list(set(bidders))
    color_palette = sns.color_palette("hsv", len(unique_bidders))

    for i, bidder in enumerate(unique_bidders):
        bidder_bids = [bid for j, bid in enumerate(bids) if bidders[j] == bidder]
        bidder_time = [time for j, time in enumerate(normalized_time) if bidders[j] == bidder]
        bidder_markers = [markers[j] for j in range(len(bidder_bids))]
        plt.scatter(bidder_time, bidder_bids, marker='o', label=f"Bidder {bidder}", color=color_palette[i])

    # Connect all bids via a line
    plt.plot(normalized_time, bids, linestyle='-', color='gray', alpha=0.7)

    # Change the vertical line to indicate the start of the active bidding stage
    plt.axvline(x=data['active_start'], color='lightgray', linestyle='--', label='Start of Active Bidding')

    plt.xlim(left=find_active_start(intervals, threshold=12000))
    plt.axvline(x=0, color="red", linestyle="--", label="Close Time")
    plt.xlabel("Time (Normalized)")
    plt.ylabel("Bids")
    plt.title(f"Price Growth Path - Item {data['original_index']}")
    plt.legend(loc='best')

    # Save the plot to a file
    plt.savefig(output_filename)
    plt.close()


# Main function to process and plot data for each item
def process_and_plot_data(filename, output_directory):
    df = pd.read_excel(filename)

    for index, row in df.iterrows():
        close_time = row['close_time']
        bids_data = eval(row['bids'])  # Convert the string to a list of lists
        normalized_time = [(bid[2] - close_time) for bid in bids_data]
        bids = [bid[1] for bid in bids_data]
        bidders = [bid[0] for bid in bids_data]

        intervals = calculate_intervals(normalized_time)
        active_start = find_active_start(intervals)

        data = {
            'original_index': row['original_index'],
            'bids': bids,
            'normalized_time': normalized_time,
            'bidders': bidders,
            'intervals': intervals,
            'active_start': active_start
        }

        output_filename = f"{output_directory}/{row['original_index']}.png"
        plot_price_growth(data, output_filename)


# Get intervals of bids from the bidding sequence to identify bidder characteristics
def get_intervals(bids, closing):
    intervals = []
    previous_time = closing

    for bid in bids:
        bidder, bid_amount, timestamp = bid

        if timestamp > closing:
            interval = timestamp - previous_time
            intervals.append(interval)

        previous_time = timestamp

    return intervals


# Output bidding intervals for each overtime rule
def extract_bidding_intervals(dataset_filename):
    data = pd.read_excel(dataset_filename)

    # Dictionary to store intervals by overtime_rule
    interval_dict = {}

    for index, row in data.iterrows():
        overtime_rule = row["overtime_rule"]
        closing_time = row["close_time"]
        bids = row["bids"]

        if overtime_rule not in interval_dict:
            interval_dict[overtime_rule] = []

        intervals = get_intervals(eval(bids), closing_time)
        interval_dict[overtime_rule].extend(intervals)

    return interval_dict


# Plot frequency distributions for overtime bidding intervals
def plot_frequency_distribution(interval_dict, overtime_rule, cutoff=60):
    intervals = interval_dict[overtime_rule]
    counter = Counter(intervals)

    x = list(counter.keys())
    y = list(counter.values())

    plt.figure(figsize=(12, 6))
    plt.bar(x, y)
    plt.title(f"Frequency Distribution for {overtime_rule} Overtime Intervals")
    plt.xlabel("Interval Duration (seconds)")
    plt.ylabel("Frequency")
    plt.xlim(0, cutoff)  # Set a cutoff for x-axis (60 seconds in this case)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()


# Plot combined CDF chart of bidding intervals used in Section 3.1
def plot_cdf(interval_dict, overtime_rule, cutoff=None):
    intervals = interval_dict[overtime_rule]
    sorted_intervals = np.sort(intervals)
    y = np.arange(1, len(sorted_intervals) + 1) / len(sorted_intervals)

    if cutoff:
        plt.plot(sorted_intervals, y, marker='.', linestyle='none', label=f'{overtime_rule} sec')
        plt.xlim(0, cutoff)
    else:
        plt.plot(sorted_intervals, y, label=f'{overtime_rule} sec')


try:
    # Plot dataset into price growth paths.
    df = "public_data/3_processed_sample_dataset.xlsx"
    process_and_plot_data(df, "output/charts")

    bidding_intervals = extract_bidding_intervals(df)

    # Create subplots for 60 seconds and 300 seconds overtime
    fig, axs = plt.subplots(1, 2, figsize=(6, 12))
    plot_frequency_distribution(bidding_intervals, 60, cutoff=60)
    axs[0].set_title("60 Seconds Overtime")

    plot_frequency_distribution(bidding_intervals, 180, cutoff=180)
    axs[1].set_title("180 Seconds Overtime")

    plt.tight_layout()
    plt.show()
    plt.close()

    cutoff = 400

    for rule in [60, 120, 180, 300]:
        plot_cdf(bidding_intervals, rule, cutoff)

    plt.title("Combined CDF for All Overtime Policies")
    plt.xlabel("Interval Duration (seconds)")
    plt.ylabel("CDF")
    plt.legend()
    plt.show()

except:
    pass