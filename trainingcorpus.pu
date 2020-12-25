"""
    Author: David Otta
    Created for: B4B33RPH
    Created on 26. 10. 2020
    Last change on 1. 11. 2020
"""
import corpus
from utils import (is_empty, read_classification_from_file)
 
 
class TrainingCorpus(corpus.Corpus):
 
    def __init__(self, path):
        super().__init__(path)
        self.spam_dict = {}
 
    def get_class(self, file_name):
        from os import sep
 
        if is_empty(self.spam_dict):
            self.spam_dict = read_classification_from_file(self.path + sep + "!truth.txt")
        return self.spam_dict.get(file_name)
 
    def is_ham(self, file_name):
        return self.get_class(file_name) == 'OK'
 
    def is_spam(self, file_name):
        return self.get_class(file_name) == 'SPAM'
 
    def hams(self):
        for file, body in self.emails():
            if self.is_ham(file):
                yield file, body
 
    def spams(self):
        for file, body in self.emails():
            if self.is_spam(file):
                yield file, body
