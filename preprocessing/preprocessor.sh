#!/bin/bash

### Preprocessing Pipeline: ###

##################################################
##### STEP 1 - Split raw pcaps into flows ########
##################################################

# Input: Raw pcaps stored in `preprocessing/data/pcaps`
# Output: `preprocessing/data/flows` directory with `tcp_syn` and `udp` subfolders

echo "------------------------------------------"
echo "STEP 1 - Splitting raw pcaps into flows..."
echo "------------------------------------------"
bash flow-splitting/flow-splitter.sh

##################################################
##### STEP 2 - Labelling                 #########
##################################################

# Input: `flows` directory with `tcp_syn` and `udp` subfolders 
# Output: `preprocessing/data/labels.csv` 

echo "---------------------"
echo "STEP 2 - Labelling..."
echo "---------------------"
bash labelling/labeller.sh

##################################################
##### STEP 3 - Extract packet payloads    ########
##################################################

# Input: `preprocessing/data/labels.csv` 
# Output: `preprocessing/data/data.csv` 

echo "-----------------------------------------------"
echo "STEP 3 - Extracting packet payloads to data.csv"
echo "-----------------------------------------------"
python3 packet-payload-extraction/packet_payload_extractor.py

#################################################################
##### STEP 4 - Create train, val, and test csv files     ########
#################################################################

# Input: `preprocessing/data/data.csv` 
# Output: `DLOGs/data/[num_classes]_[num_packets_per_class]/(train|val|test)_[num_classes]_[num_packets_per_class].csv` files 

echo "------------------------------------------------"
echo "STEP 4 - Creating train, val, and test csv files"
echo "------------------------------------------------"
python3 train-val-test-data-construction/train-val-test-splitter.py