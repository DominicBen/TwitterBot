import argparse
# Other Files
from model import *
from dataset import *


parser = argparse.ArgumentParser()
parser.add_argument('--epochs', type=int, default=50)
parser.add_argument('--batchsize', type=int, default=128)
parser.add_argument('--sequencelength', type=int, default=5)
parser.add_argument('--twitteruser', type=ascii, default='AndyOnTheNet')
parser.add_argument('--numoftweets', type=int, default=50)
parser.add_argument('--temperature', type=int, default=0.5)
parser.add_argument('--lr', type=float, default=0.001)
parser.add_argument('--generatedtweetlength', type=float, default=20)

args = parser.parse_args()

dataset = Dataset(args)

model = Model(dataset)
train(dataset, model, args)
for x in range(10):
     
    print(predict(dataset, model, next_words=args.generatedtweetlength, temperature=args.temperature , text='i am' ))
