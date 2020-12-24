"""
    Author: David Otta
    Created for: B4B33RPH
    Created on 03. 10. 2020
    Last change on 04. 11. 2020
"""
import corpus


class BaseFilter:
    def __init__(self):
        self.path = None
        self.spam_senders = []
        self.spam_dict = {}
        self.prediction_dictionary = {}
        self.answer = "OK"

    def train(self, path):
        return None, None

    def test(self, path):
        from os import sep
        with open(path + sep + "!prediction.txt", "w", encoding="utf-8") as fw:
            my_corpus = corpus.Corpus(path)
            for mail_name, mail_text in my_corpus.emails():
                fw.write(f"{mail_name} {self.answer}\n")
