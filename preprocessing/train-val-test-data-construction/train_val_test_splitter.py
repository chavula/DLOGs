import pandas as pd
import matplotlib.pyplot as plt
import sklearn
from sklearn.model_selection import train_test_split
import logging
import os

#Original file
CLASSES = ["YouTube", "Amazon", "Facebook", "GoogleServices", "Instagram", "WhatsApp", "NetFlix", "BitTorrent", "TeamViewer", "GMail", "PlayStore", "Messenger", "Pinterest", "Ookla", "WindowsUpdate", "Microsoft", "UbuntuONE", "QUIC"]
PACKETS_PER_CLASS = 10000
RANDOM_STATE = 42

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s  %(message)s',
                    datefmt='%H:%M:%S')
logger = logging.getLogger("logger")

# Read in the csv with byte_array - label pairs
logger.info("Reading in the csv with all packets")
df = pd.read_csv('./../data/data.csv')
logger.info("Reading csv complete")

# Sample PACKETS_PER_CLASS packets from each class in CLASSES and add to df_new
df_new = pd.DataFrame()
for label in CLASSES:
    logger.info("Sampling {0} packets from {1}".format(PACKETS_PER_CLASS,
                                                       label))
    # e.g. if label == Facebook, extract the Facebook rows
    df_label = df[df["label"] == label]
    # e.g. make sure at least 10000 Facebook packets
    assert len(df_label) >= PACKETS_PER_CLASS
    df_sampled = df_label.sample(n=PACKETS_PER_CLASS,
                                 random_state=RANDOM_STATE)
    df_new = df_new.append(df_sampled)

# Zero-pad packets that have fewer than 1480 bytes in the packets
logger.info("Zero-padding the packets")
df_new.fillna(0, inplace=True)

# Split into train, val and test sets, using stratified splits to preserve balance in classes
logger.info("Splitting into training, validation and testing sets")
df_train, df_test = train_test_split(df_new, test_size=0.2,
                                     random_state=RANDOM_STATE,
                                     stratify=df_new["label"])
df_train, df_val = train_test_split(df_train, test_size=0.2,
                                    random_state=RANDOM_STATE,
                                    stratify=df_train["label"])

# Write to the train and test csv's named using the format:
#   [NUM_CLASSES]_[PACKETS_PER_CLASS]_['train'|'test'].csv
logger.info("Writing to csv's")

file_suffix = "{0}_{1}".format(len(CLASSES), PACKETS_PER_CLASS)  # e.g. 3_10000

try:
    os.mkdir("./../data/{0}/".format(file_suffix))
except OSError as error:
    print(error)

df_train.to_csv("./../data/{0}/train_{0}.csv".format(file_suffix),
                index=False)
logger.info("train_{0}.csv created".format(file_suffix))

df_val.to_csv("./../data/{0}/val_{0}.csv".format(file_suffix),
              index=False)
logger.info("val_{0}.csv created".format(file_suffix))

df_test.to_csv("./../data/{0}/test_{0}.csv".format(file_suffix),
               index=False)
logger.info("test_{0}.csv created".format(file_suffix))
