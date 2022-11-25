# Note: Write down the parser class in the separated file, redial_parser.
# Since we want the word2vec notebook to contain the context of parser, we put the writefile to do that.

from copy import deepcopy

import json
import pandas


def load_data(path):
    """
    TODO: initialization function for dataset reads

        :arg
            path (str): Dataset path.
        :return
            tuple: (train, test, df_mention)
    """
    train_data = []
    for line in open(f"{path}/train_data.jsonl", "r"):
        train_data.append(json.loads(line))

    test_data = []
    for line in open(f"{path}/test_data.jsonl", "r"):
        test_data.append(json.loads(line))

    mention_dataframe = pandas.read_csv(f"{path}/movies_with_mentions.csv")

    return train_data, test_data, mention_dataframe



class RedialParser:
    def __init__(self, path):
        self.train, self.test, self.movie = load_data(path)

        self.__train = deepcopy(self.train)
        self.__test = deepcopy(self.test)
        self.__movie = deepcopy(self.movie)

        self.__model = None

    def Restore(self):
        """
        TODO: Restore train, test, and movie dataset to initial state
        """
        self.train = deepcopy(self.__train)
        self.test = deepcopy(self.__test)
        self.movie = deepcopy(self.__movie)

    def Movies(self, train=True) -> dict:
        """
        TODO: Get movie list in dataset

            :arg
                train (bool): Target dataset, (train=True, test=False, all=None)
            :return
                dict: {index, MovieName}
        """
        if train is None:
            result = self.Movies()
            result.update(self.Movies(False))
            return result

        target = None
        if train is True:
            target = self.train
        elif train is False:
            target = self.test

        result = {}

        if target is not None:
            for elem in target:
                result.update(elem['movieMentions'])

        return result

    def describe(self):
        """
        TODO: Describe its datasets
        """
        len1, len2 = len(self.train), len(self.test)
        n1, n2 = 0, 0
        m1, m2 = 0, 0

        for e in self.train:
            n1 += len(e['movieMentions'])
            m1 += len(e['messages'])
        for e in self.test:
            n2 += len(e['movieMentions'])
            m2 += len(e['messages'])

        print('Brief information:\n'
              f'Length of train data: {len1}\n'
              f'Length of test data: {len2}\n\n'
              'Data information:\n'
              f'Key parameters: {list(self.train[0].keys())}\n'
              f'Key parameters in Questions: {list(list(self.train[0]["respondentQuestions"].values())[0].keys())}\n'
              f'Key parameters in messages: {list(self.train[0]["messages"][0].keys())}\n\n'
              'Context information:\n'
              f'Total mentioned movie number (train): {n1}\n'
              f'Total mentioned movie number in unique (train): {len(self.Movies())}\n'
              f'Total message number (train): {m1}\n'
              f'Total mentioned movie number (test): {n2}\n'
              f'Total mentioned movie number in unique (test): {len(self.Movies(False))}\n'
              f'Total message number (test): {m2}\n'
              f'Average mentioned movie numbers per conversation (train): {n1 / len1}\n'
              f'Average message numbers per conversation (train): {m1 / len1}\n'
              f'Average mentioned movie numbers per conversation (test): {n2 / len2}\n'
              f'Average message numbers per conversation (test): {m2 / len2}\n\n'
              , end='')

