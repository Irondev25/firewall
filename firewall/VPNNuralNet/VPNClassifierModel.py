import torch

class Feedforward(torch.nn.Module):
    def __init__(self, input_size, h1, h2):
            super(Feedforward, self).__init__()
            self.input_size = input_size
            self.h1 = h1
            self.h2 = h2
            self.fc1 = torch.nn.Linear(self.input_size, self.h1)
            self.fc2 = torch.nn.Linear(self.h1, self.h2)
            self.fc3 = torch.nn.Linear(self.h2,1)

            self.relu = torch.nn.ReLU()
            self.dropout = torch.nn.Dropout(p=0.1)
            self.sigmoid = torch.nn.Sigmoid()
            self.batchnorm1 = torch.nn.BatchNorm1d(self.h1)
            self.batchnorm2 = torch.nn.BatchNorm1d(self.h2)
 
    def forward(self, x):
        #1st pass
        x = self.relu(self.fc1(x))
        x = self.batchnorm1(x)
        x = self.relu(self.fc2(x))
        x = self.batchnorm2(x)
        x = self.dropout(x)
        x = self.fc3(x)
        return x