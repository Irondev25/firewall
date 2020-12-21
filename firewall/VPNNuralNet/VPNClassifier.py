import torch.nn as nn
import torch
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


from .VPNClassifierModel import Feedforward
from .DatasetLoader import FeatureDataset

listOfFeatureIndex = [9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,26,27,28,29,30,31,32,33,38,39,40,41,42,43]
metadata = [0,1,2,3]

def evalualte(file_name):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # init_dataset = FeatureDataset(file_name)
    # dataset = torch.utils.data.DataLoader(init_dataset,batch_size=1)

    # model = Feedforward(30,15,1)
    # model.load_state_dict(torch.load('saved_model/VPNClassifier'))
    # model.eval()

    # with torch.no_grad():
    #     for X_batch,y_batch in dataset:
    #         print(X_batch[0],X_batch[1],X_batch[2],X_batch[3])
    #         if((X_batch[0] == '127.0.0.1' and X_batch[1] == '8000') or (X_batch[2] == '127.0.0.1' and X_batch[3] == '8000')):
    #             X_batch,y_batch = X_batch.to(device), y_batch.to(device)
    #             y_pred = model(X_batch)
    #             y_pred = torch.round(torch.sigmoid(y_pred))
    #             return y_pred
    file_out = pd.read_csv(file_name)
    x = file_out.iloc[-1,listOfFeatureIndex].values
    x = np.reshape(x,(1,-1))
    meta = file_out.iloc[-1,metadata].values

    sc = StandardScaler()
    x_train = sc.fit_transform(x)
    X_train = torch.FloatTensor(x_train)

    model = Feedforward(30,15,1)
    model.load_state_dict(torch.load('firewall/VPNNuralNet/saved_model/VPNClassifier'))
    model.eval()

    with torch.no_grad():
        print(X_train[0])
        print(meta)
        # if((X_batch[0][0] == '127.0.0.1' and X_batch[][1] == '8000') or (X_batch[2] == '127.0.0.1' and X_batch[3] == '8000')):
        X_batch = X_train
        X_batch = X_batch.to(device)
        y_pred = model(X_batch)
        y_pred = torch.round(torch.sigmoid(y_pred))
        return y_pred
