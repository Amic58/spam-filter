"""
    Author: David Otta
    Created for: B4B33RPH
    Created on 26. 10. 2020
    Last change on 02. 11. 2020
"""

SPAM_TAG = "SPAM"
HAM_TAG = "OK"

def read_classification_from_file(file_name):
    """
        Filename contains 'mail_file_name OK/SPAM\n'
        return: dict with 'mail_file_name': OK/SPAM
    """
    _dict = {}
    with open(file_name, 'r', encoding='utf-8') as fr:
        while fr:
            line = fr.readline()
            if line == "":
                break
            line_data = line.rstrip().split()
            _dict[line_data[0]] = line_data[1]
    return _dict


def html_clean(word):
    return word.replace("<br>", "").replace("</br>", "").strip(['<', '>'])


def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True
