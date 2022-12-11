import argparse
import torch
import numpy as np
from predict import *
from model import Model
from torch import nn, optim
from torch.utils.data import DataLoader

from dataset import Dataset
def train(dataset, model, args):
    model.train()
    dataloader = DataLoader(dataset, batch_size=args.batch_size)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    for epoch in range(args.max_epochs):
        state_h, state_c = model.init_state(args.sequence_length)
        for batch, (x, y) in enumerate(dataloader):
            optimizer.zero_grad()
            y_pred, (state_h, state_c) = model(x, (state_h, state_c))
            loss = criterion(y_pred.transpose(1, 2), y)
            state_h = state_h.detach()
            state_c = state_c.detach()
            loss.backward()
            optimizer.step()
            print({ 'epoch': epoch, 'batch': batch, 'loss': loss.item() })

parser = argparse.ArgumentParser()
parser.add_argument('--max-epochs', type=int, default=100)
parser.add_argument('--batch-size', type=int, default=256)
parser.add_argument('--sequence-length', type=int, default=4)
parser.add_argument('--twitter-user', type=ascii, default="realDonaldTrump")
parser.add_argument('--numoftweets', type=int, default=20)

args = parser.parse_args()

dataset = Dataset(args)

model = Model(dataset)
train(dataset, model, args)
print(predict(dataset, model, text='I want you to know'))