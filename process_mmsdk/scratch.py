import csv

def convert(number):
    if number == -3:
        return 0
    elif number == -2:
        return 1
    elif number == -1:
        return 2
    elif number == 0:
        return 3
    elif number == 1:
        return 4
    elif number == 2:
        return 5
    elif number == 3:
        return 6


with open("process_mmsdk/mosei_dataset_int.csv", "r") as rf:
    csvreader = csv.reader(rf)
    next(csvreader)
    with open("process_mmsdk/no_sentiment.csv", "w", newline="") as wf:
        csvwriter = csv.writer(wf)
        headers = ["video_name_segment", "happy", "sad", "anger", "surprise", "disgust", "fear"]
        csvwriter.writerow(headers)
        for row in csvreader:
            # sentiment = int(row[1])
            # new_sentiment = convert(sentiment)
            csvwriter.writerow([row[0], row[2], row[3], row[4], row[5], row[6], row[7]])

        