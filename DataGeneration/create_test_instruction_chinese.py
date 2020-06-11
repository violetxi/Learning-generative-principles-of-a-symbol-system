""" 
This script is used to create testing sets for various conditions:
1. Old - S, MD, MS_no_T, MS_T, ALL
2. New - S, MD, MS_no_T, MS_T, ALL
each of them has an instruction file.
Also output a csv file containing trial number and image names and 
numbers in the image,
"""
import os
import cv2
import argparse
import numpy as np
import pandas as pd

from num2words import num2words

# Load testing set and separate them into three groups
def process_input(in_f):
    df_in = pd.read_csv(in_f)
    # A list of number pairs for each category
    old_pairs = {'S':[], 'MD':[], 'MS_no_T':[], 'MS_T':[], 'All':[]}
    new_pairs = {'S':[], 'MD':[], 'MS_no_T':[], 'MS_T':[], 'All':[]}
    # Fill out the list of the number pairs, each pair has (target
    for index, row in df_in.iterrows():
        num_pair = (row["target"], row["foil"])
        label_pair = (row["target_correct_label"], row["foil_correct_label"])
        if row["old_or_new"] == 'old':
            old_pairs['All'].append([num_pair, label_pair])
            old_pairs[row['category']].append([num_pair, label_pair])
            
        else:
            new_pairs['All'].append([num_pair, label_pair])
            new_pairs[row['category']].append([num_pair, label_pair])
    return old_pairs, new_pairs

# Create 10 instructions based on new_ and old_pairs and 
# also save trial number, img names and its correpsonding
# numbers to a csv file
def create_instruction(testing_pairs, out, ftype):
    for t in testing_pairs.keys():
        out_tiral = os.path.join(out, "trial_{}_{}.csv".format(ftype, t))
        out_instr = os.path.join(out, "test_{}_{}.csv".format(ftype, t))
        # Create empty data frames for trial and test instruction files (testing freq is 1 for all numbers)
        instr_df = pd.DataFrame(columns=["visual", "word", "frequency"], index=np.arange(0, len(testing_pairs[t])*2))
        trial_df = pd.DataFrame(columns=["image_name", "number_target", "word_target", "number_foild", "word_foil"], index=np.arange(0, len(testing_pairs[t])))
        # Add pairs to trial_df and each number to instruction
        # i is used to keep track of image name
        num_trial, i = 0, 0
        for num_label_pair in testing_pairs[t]:
            num_pair, label_pair = num_label_pair         
            # Target
            target = num_pair[0]
            target_word = label_pair[0]
            # Foil
            foil = num_pair[1]
            foil_word = label_pair[1]
            # Save target number and words to instruction
            instr_df.loc[i] = [target, target_word, 1]
            target_img = "{}.png".format(str(i))
            i += 1
            # Save foil number and words to instruction
            instr_df.loc[i] = [foil, foil_word, 1]
            foil_img = "{}.png".format(str(i))
            i += 1
            # Save target and foil to trial file
            trial_df.loc[num_trial] = ["{} {}".format(target_img, foil_img), target, target_word, foil, foil_word]
            num_trial += 1
        print("Saving tiral to {}".format(out_tiral))
        trial_df.to_csv(out_tiral)
        print("Saving instruction to {}".format(out_instr))
        instr_df.to_csv(out_instr)

##### Parsing arguments #####
parser = argparse.ArgumentParser(description='Process command line optional inputs')
parser.add_argument('--input_file', '-i', help="Input data file if want to create certain numbers")
parser.add_argument('-out',  '-o',help="Output directory")
args = parser.parse_args()
old_pairs, new_pairs = process_input(args.input_file)
create_instruction(old_pairs, args.out, 'old')
create_instruction(new_pairs, args.out, 'new')
