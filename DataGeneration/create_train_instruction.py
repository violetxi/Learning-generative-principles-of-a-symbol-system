"""
This script is used to create training instruction, which is later 
used to create training images and labels for number recognition 
task. Command line input:
1). input_file: the pre-existing dataset instructions
2). out: output instruction for training (visual,word, frequency) csv format
** Note: need to manually add a '-' between ** and hundred as well as ** and 
thousand
"""
import os
import cv2
import argparse
import numpy as np
import pandas as pd

from num2words import num2words

# Load a csv file containing the training number, then create
# training instruction.
def create_instruction(csv_in, out, freq):
    df_in = pd.read_csv(csv_in)
    # A new data frame that will be used as output
    df_out = pd.DataFrame(columns=["visual", "word", "frequency"], index=df_in.index.values.tolist())
    for index, row in df_in.iterrows():
        # Remove 'and' and remove - between tys
        word = num2words(row["number"]).replace(' and', '')
        word = word.replace(',', '')
        word = word.replace('-', ' ')
        df_out["visual"][index] = row["number"]
        df_out["frequency"][index] = freq
        df_out["word"][index] = word
    df_out.to_csv(out)

##### Parsing arguments #####
parser = argparse.ArgumentParser(description='Process command line optional inputs')
parser.add_argument('--input_file', '-i', help="Input data file if want to create certain numbers")
parser.add_argument('--out',  '-o',help="Output directory")
parser.add_argument('--freq', '-f', type=int, help="Frequency of the numbers")
args = parser.parse_args()
create_instruction(args.input_file, args.out, args.freq)
