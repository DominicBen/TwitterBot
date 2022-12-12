import argparse
# Other Files
from model import *
from dataset import *


parser = argparse.ArgumentParser()
parser.add_argument('--maxepochs', type=int, default=20)
parser.add_argument('--batchsize', type=int, default=256)
parser.add_argument('--sequencelength', type=int, default=4)
parser.add_argument('--twitteruser', type=ascii, default='realDonaldTrump')
parser.add_argument('--numoftweets', type=int, default=20)
parser.add_argument('--temperature', type=int, default=0.8)
parser.add_argument('--lr', type=float, default=0.001)

args = parser.parse_args()

dataset = Dataset(args)

model = Model(dataset)
train(dataset, model, args)
print(predict(dataset, model, temperature=args.temperature , text='i am' ))