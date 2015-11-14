# -*- coding: utf-8 -*-


class FeelingCalculate:

    feelings = {}

    def calculate(self, mention_text):

        feeling_value = sum(map(lambda word: self.feelings.get(word, 0), mention_text.split()))

        return feeling_value

    def _load_feelings(self, file_name):

        for feeling_line in open('./../feelings/' + file_name):
            try:
                feeling = feeling_line.split('\t')
                self.feelings[feeling[0]] = int(feeling[1])

            except IndexError:
                print feeling_line

    def __init__(self):
        self._load_feelings('english.txt')
        self._load_feelings('portuguese.txt')
