__author__ = 'wwang'

def year_to_number(year_str):
    year_num = 2 * ord(year_str[0]) - 1
    year_char_val = 0 if year_str[1] == 'A' else 1
    return year_num + year_char_val

def year_to_str(year_number):
    year_num = (year_number + 1) / 2
    year_char = 'A' if year_num % 2 == 1 else 'B'
    return str(year_num) + str(year_char)