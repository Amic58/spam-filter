"""
    Author: David Otta
    Created for: B4B33RPH
    Created on 10. 10. 2020
    Last change on 11. 11. 2020
"""
import basefilter_new


class MyFilter(basefilter_new.BaseFilter):
    def __init__(self):
        super().__init__()
        self.prediction_file_name = "!prediction.txt"
        self.spam_word_freq = {}
        self.spam_senders = []
        self.border_value = 0
        self.spam_sender_multiplier = 3

    def train(self, path):
        from trainingcorpus import TrainingCorpus

        training_corpus = TrainingCorpus()
        spam_dict = {}
        ham_dict = {}

        self.train_on_group(training_corpus.spams, spam_dict, spam=True)
        self.train_on_group(training_corpus.hams, ham_dict, spam=False)

        dict_diff = self.create_testing_spam_dict(ham_dict, spam_dict)

        self.spam_word_freq = dict_diff

    def create_testing_spam_dict(self, ham_dict, spam_dict):
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
        for name, body in get_emails():
            self.train_on_text(body, eval_dict, spam)

    def train_on_text(self, text, eval_dict, spam=False):
        from utils import html_clean

        sender_flag = False
        words = text.split()
        # evaluate all words
        for word in words:
            # sort out html like keywords
            if word.startswith("<") and word.endswith(">") or '@' in word:
                html_clean(word)
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

        with open(path + "!prediction", "w", encoding="utf-8") as fw:
            for name, pred in prediction:
                fw.write(f"{name} {pred}\n")

    def append_result_dict(self, prediction: list, spam_index, file_name):
        if spam_index >= 0:
            prediction.append((file_name, "SPAM"))
        else:
            prediction.append((file_name, "OK"))

    def evaluate_mail(self, words):
        from utils import html_clean

        sender_flag = False
        spam_sender_flag = False
        spam_score = 0
        # evaluate all words
        for word in words:
            # sort out html like keywords
            if word.startswith("<") and word.endswith(">") or '@' in word:
                html_clean(word)
            if word == "":
                continue

            if word in self.spam_dict:
                spam_score += self.spam_dict[word]
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
