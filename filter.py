"""
    Author: David Otta
    Created for: B4B33RPH
    Created on 10. 10. 2020
    Last change on 10. 12. 2020
"""
import basefilter
import utils
from os import sep


class MyFilter(basefilter.BaseFilter):
    def __init__(self):
        super().__init__()
        self.prediction_file_name = "!prediction.txt"
        self.spam_word_freq = {}
        self.spam_senders = []
        self.border_value = 10000
        self.spam_sender_multiplier = 5

    def train(self, path):
        """
        Trains filter on given data.
        :param path: directory with
        :return: no return
        """
        from trainingcorpus import TrainingCorpus

        training_corpus = TrainingCorpus(path)
        spam_dict = {}
        ham_dict = {}

        self.train_on_group(training_corpus.spams, spam_dict, spam=True)
        self.train_on_group(training_corpus.hams, ham_dict, spam=False)

        dict_diff = self.create_testing_spam_dict(ham_dict, spam_dict)

        self.spam_word_freq = dict_diff

    def create_testing_spam_dict(self, ham_dict, spam_dict):
        """
        Combines dictionaries with spam words and ham words
        :param ham_dict: dictionary with ham word frequencies
        :param spam_dict: dictionary with spam word frequencies
        :return: dictionary with difference of spam and ham dictionaries
        """
        spam_ham_diff = {}
        # create spam dictionary for testing
        for key in spam_dict:
            ham_val = ham_dict.get(key)
            if not ham_val:
                ham_val = 0

            spam_ham_diff[key] = spam_dict[key] - ham_val
        for key in ham_dict:
            if key not in spam_dict:
                spam_ham_diff[key] = -ham_dict[key]

        return spam_ham_diff

    def train_on_group(self, get_emails, eval_dict, spam=False):
        """
        Trains on single emails.
        :param get_emails: generator function
        :param eval_dict: dict to store training results
        :param spam: are we training on spam
        :return: no return
        """
        for name, body in get_emails():
            self.train_on_text(body, eval_dict, spam)

    def train_on_text(self, text, eval_dict, spam=False):
        """
        Train on text of an email.
        :param text: text of an email
        :param eval_dict: dict to store results in
        :param spam: is it spam
        :return: no return
        """
        sender_flag = False
        words = text.split()
        # evaluate all words
        for word in words:
            word.lower()
            # sort out html like keywords
            if word.startswith("<") and word.endswith(">") or '@' in word:
                utils.html_clean(word)
            if word == "":
                continue

            # save sender
            if sender_flag:
                if '@' in word:
                    if spam:
                        self.spam_senders.append(word)
                    sender_flag = False
                continue
            # raise from flag
            if word == "From:":
                sender_flag = True
                continue

            if word not in eval_dict:
                eval_dict[word] = 1
            else:
                eval_dict[word] = eval_dict.get(word) + 1

    def test(self, path):
        from corpus import Corpus

        corpus = Corpus(path)
        prediction = []

        for name, body in corpus.emails():
            spam_index, spam_sender_flag = self.evaluate_mail(body.split())
            spam_index += spam_sender_flag * self.spam_sender_multiplier * len(body.split())

            self.append_result_dict(prediction, spam_index, name)

        with open(path + sep + self.prediction_file_name, "w", encoding="utf-8") as fw:
            for name, pred in prediction:
                fw.write(f"{name} {pred}\n")

    def append_result_dict(self, prediction: list, spam_index, file_name):
        """
        Append dictionary with results.
        :param prediction: list of predictions
        :param spam_index: number, that desceibes how spammness of a file
        :param file_name: name of the file
        :return:
        """
        if spam_index >= self.border_value:
            prediction.append((file_name, utils.SPAM_TAG))
        else:
            prediction.append((file_name, utils.HAM_TAG))

    def evaluate_mail(self, words):
        """
        Run evaluation based on whether it was trained on not.
        :param words: list of all words in an email
        :return: evaluation result
        """
        # if MyFilter not trained
        res = tuple()

        if self.spam_word_freq == {}:
            res = self.evaluate_mail_not_trained(words)
        else:
            res = self.evaluate_mail_trained(words)

        return res

    def evaluate_mail_not_trained(self, words):
        from random import choice

        return len(words) * choice([-1, 1]), choice([True, False])

    def evaluate_mail_trained(self, words):
        sender_flag = False
        spam_sender_flag = False
        spam_score = 0
        # evaluate all words
        for word in words:
            word.lower()
            # sort out html like keywords
            if word.startswith("<") and word.endswith(">") or '@' in word:
                utils.html_clean(word)
            if word == "":
                continue

            if word in self.spam_word_freq:
                spam_score += self.spam_word_freq[word]
                continue

            # save sender
            if sender_flag:
                if '@' in word and word in self.spam_senders:
                    spam_sender_flag = True
                sender_flag = False
                continue
            # raise from flag
            if word == "From:":
                sender_flag = True
                continue
        return spam_score, spam_sender_flag
