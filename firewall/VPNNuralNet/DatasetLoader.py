import pandas as pd 
import torch
from torch.utils.data import Dataset
from sklearn.preprocessing import StandardScaler

listOfFeatureIndex = [9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,26,27,28,29,30,31,32,33,38,39,40,41,42,43]

class FeatureDataset(Dataset):

    def __init__(self,file_name):
        file_out = pd.read_csv(file_name)
        self.x = file_out.iloc[:,listOfFeatureIndex].values
        self.y = file_out.iloc[:,44].values

        # print(x[:5,:])
        # print(y[:5])
        # label = {'Non-VPN':0,'VPN':1}
        # y = [label[item] for item in y]
        sc = StandardScaler()
        self.x_train = sc.fit_transform(self.x)
        self.y_train = self.y
        # for item in x[-10:]:
        #     print(item)
        # for item in y[-10:]:
        #     print(item)
        self.X_train = torch.FloatTensor(self.x_train)
        self.Y_train = torch.FloatTensor(self.y_train)
    
    def __len__(self):
        return len(self.Y_train)
    
    def __getitem__(self,idx):
        return self.X_train[idx],self.Y_train[idx]

# feature_dataset = FeatureDataset('datasetv2/dataset_for_mlp_full.csv')