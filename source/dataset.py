import torch
import pandas as pd
from twitterapi import *
from collections import Counter
class Dataset(torch.utils.data.Dataset):
    def __init__(self,args):
        self.args = args
        self.words = self.load_words()
        self.uniq_words = self.get_uniq_words()
        # converts an index in a vocab to a word
        self.itow = {index: word for index, word in enumerate(self.uniq_words)}
        # converts a word from a vocab to an index
        self.wtoi = {word: index for index, word in enumerate(self.uniq_words)}
        # converts our list of tweets into indexes
        self.words_indexes = [self.wtoi[w] for w in self.words]
    def load_words(self):
        # Grabs a single 1d array of tweets seperated by word as our dataset. 
        text = grab(self.args.twitteruser[1:-1],self.args.numoftweets)
        # text = grabdataset(self.args.twitteruser[1:-1],self.args.numoftweets)
        return text
        
    def get_uniq_words(self):
        word_counts = Counter(self.words)
        return sorted(word_counts, key=word_counts.get, reverse=True)

    def __len__(self):
        return len(self.words_indexes) - self.args.sequencelength
    # predefined 
    def __getitem__(self, index):
        return (
            torch.tensor(self.words_indexes[index:index+self.args.sequencelength]),
            torch.tensor(self.words_indexes[index+1:index+self.args.sequencelength+1]),
        )