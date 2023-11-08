from random import sample


# Stage 3 - Additional Functions to Sample Data

# summarizes data
def summary_auction_data(data):
    print(len(data))

    def count_overtime(numbers):
        a, b, c, d = 0, 0, 0, 0
        for number in numbers:
            if number == 60:
                a += 1
            elif number == 120:
                b += 1
            elif number == 180:
                c += 1
            elif number == 300:
                d += 1
        return [a, b, c, d, sum([a, b, c, d])]

    print(count_overtime(data['overtime_rule']))
    data_subset = data[data['is_overtime_item'] == True]
    print(count_overtime(data_subset['overtime_rule']))


# sample 3-minute overtime items by returning a list of sampled items index
def sample_overtime_items(data):
    overtime_6 = []
    overtime_1 = []
    all_rest = []
    for i in data.iterrows():
        if i[1]['is_overtime_item']:
            if i[1]['overtime_rule'] == 180:
                if int(i[1]['auction_no']) // 1000 == 6:
                    overtime_6.append(i[0])
                elif int(i[1]['auction_no']) // 1000 == 1:
                    overtime_1.append(i[0])
            else:
                all_rest.append(i[0])
    len_1 = len(overtime_1)
    len_6 = len(overtime_6)
    seq_1 = sample(overtime_1, len_1 // 2)
    seq_6 = sample(overtime_6, len_6 // 2)
    all_sampled = seq_1 + seq_6 + all_rest
    all_sampled.sort()
    return data.iloc[all_sampled]
