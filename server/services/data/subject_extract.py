__author__ = 'wwang'

import re
import os

# simply script to process texts copy from http://ugradcalendar.uwaterloo.ca/page/Course-Descriptions-Index

subjuct_input_file = open(os.path.dirname(os.path.realpath(__file__)) + '/subject_list_raw.txt', 'r')
subject_str = subjuct_input_file.read()
subject_tuples = re.findall(r'(.+?)\t(.+?)(\s|\t)(\s|\t)?(AHS|ART|ENG|ENV|MAT|SCI|REN|VPA|WLU)', subject_str)
print 'get ' + str(len(subject_tuples)) + ' subjects.'
subjuct_output_file = open(os.path.dirname(os.path.realpath(__file__)) + '/subject_list_pair.txt', 'w')
for tuple in subject_tuples:
    subjuct_output_file.write(tuple[0].rstrip() + '|' + tuple[1] + "\n")

subjuct_output_file.close()
# Validate
# with open(os.path.dirname(os.path.realpath(__file__)) + '/subject_list.txt', 'r') as f1:
#     with open(os.path.dirname(os.path.realpath(__file__)) + '/subject_list2.txt', 'r') as f2:
#         l1 = f1.read().splitlines()
#         l2 = f2.read().splitlines()
#         print len(l1)
#         print len(l2)
#         for i in range(0, 114):
#             if l1[i] != l2[i][-len(l1[i]):]:
#                 print l1[i]
