__author__ = 'wwang'

import re
import os

subjuct_input_file = open(os.path.dirname(os.path.realpath(__file__)) + '/subject_list_raw.txt', 'r')
subject_str = subjuct_input_file.read()
subject_pair = re.findall(r'\t(.+?)(\s|\t)(\s|\t)?(AHS|ART|ENG|ENV|MAT|SCI|REN|VPA|WLU)', subject_str)
print 'get ' + str(len(subject_pair)) + ' subjects.'
subjuct_output_file = open(os.path.dirname(os.path.realpath(__file__)) + '/subject_list.txt', 'w')
for pair in subject_pair:
    subjuct_output_file.write(pair[0] + "\n")