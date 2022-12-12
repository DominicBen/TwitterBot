import torch
import time
import torch.nn as nn
import torch.optim as OPT
import numpy as np
from torch import nn
from torch.utils.data import DataLoader
import torch.nn.functional as FF
#other files
from dataset import Dataset
class Model(nn.Module):
    def __init__(self, dataset, use_gpu = False, lstm_size = 128, embedding_size = 128 , num_layers = 3, hidden_size = 100, dropout = 0.2 ):
        super(Model, self).__init__()
        self.lstm_size = lstm_size
        self.embedding_size = embedding_size
        self.num_layers = num_layers
        self.vocabsize = len(dataset.uniq_words)
        self.hidden_size = hidden_size
        self.dropout = dropout

        # Set tensor type when using GPU
        if use_gpu:
            self.float_type = torch.cuda.FloatTensor
            self.long_type = torch.cuda.LongTensor
            torch.cuda.manual_seed_all(2)
        # Set tensor type when using CPU
        else:
            self.float_type = torch.FloatTensor
            self.long_type = torch.LongTensor

        np.random.seed(2)
        torch.manual_seed(2)


        # embedding layer
        self.embedding = nn.Embedding(
            num_embeddings=self.vocabsize,
            embedding_dim=self.embedding_size,
        )
        # LSTM layer
        self.lstm = nn.LSTM(
            input_size=self.embedding_size,
            hidden_size=self.lstm_size,
            num_layers=self.num_layers,
            dropout=self.dropout,
        )
         # The fully connected layers
        self.linear1 = nn.Linear(self.lstm_size, self.hidden_size)
        self.linear2 = nn.Linear(self.hidden_size, self.hidden_size)
        self.linear3 = nn.Linear(self.hidden_size, self.hidden_size)
        # Final Softmax layer to our dictionary
        self.linear4 = nn.Linear(self.hidden_size, self.vocabsize)

    # forward propagation
    def forward(self, x, prev_state):
        embed = self.embedding(x)
        lstm_output, state = self.lstm(embed, prev_state)

        output = FF.dropout(FF.tanh(self.linear1(lstm_output)), p=self.dropout)
        output = FF.dropout(FF.tanh(self.linear2(output)), p=self.dropout)
        output = FF.dropout(FF.tanh(self.linear3(output)), p=self.dropout)


        output = self.linear4(output)

        return output, state
      
    def init_state(self, sequence_length):
        return (torch.zeros(self.num_layers, sequence_length, self.lstm_size),
                torch.zeros(self.num_layers, sequence_length, self.lstm_size))


def train(dataset, model, args):
    model.train()
    start_time = time.time()

    dataloader = DataLoader(dataset, batch_size=args.batchsize)
    criterion = nn.CrossEntropyLoss()
    optimizer = OPT.Adam(model.parameters(), lr=args.lr)

    for epoch in range(args.maxepochs):
        h, c = model.init_state(args.sequencelength)
        for batch, (index, value) in enumerate(dataloader):
            y_pred, (h, c) = model(index, (h, c))
            #loss = criterion(y_pred.transpose(1, 2), value)

            
            loss = FF.nll_loss(y_pred.transpose(1, 2), value)
            h = h.detach()
            c = c.detach()

            # Zero gradients, perform a backward pass, and update the weights.
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()


            print({ 'epoch': epoch, 'batch': batch, 'loss': loss.item() })
    
    end_time = time.time()
    print ('the training took: %d(s)' % (end_time - start_time))

# Takes in a softmax probability distribution and chooses a the value with the highest probabiltiy
# Also adds temperature which gives slight randomness to this desision
# temperature = 1.0 Random
# temperature = 0.0 conservitive 
# Grabbed from https://keras.io/examples/lstm_text_generation/

def sample(preds, temperature = 0.8):
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)



# Takes in a NN model, and dataset, and generates the next likely word in that data set
def predict(dataset, model, temperature, text, next_words=100 ):
    model.eval()
    words = text.split(' ')
    h, c = model.init_state(len(words))
    for i in range(0, next_words):
        x = torch.tensor([[dataset.word_to_index[w] for w in words[i:]]])
        y_pred, (h, c) = model(x, (h, c))
        prediction = y_pred[0][-1]
        print(prediction)
        predictionsoftmax = FF.softmax(prediction, dim=0).detach().numpy()
        word_index = sample(predictionsoftmax,temperature)
        words.append(dataset.index_to_word[word_index])
    return words