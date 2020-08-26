import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

def cut_dolar(text):
    return text[1:]
initial_df = pd.read_csv("DJ/dow_jones_index.data")

df = initial_df[['stock','date','open','high','low','close','volume']]
for i in range(len(df)):
    df.at[i,'high'] = cut_dolar(df.iloc[i]['high'])
    df.at[i,'low'] = cut_dolar(df.iloc[i]['low'])
    df.at[i,'close'] = cut_dolar(df.iloc[i]['close'])
    df.at[i,'open'] = cut_dolar(df.iloc[i]['open'])

for i in range(len(df)):
    df.at[i,'h_o'] = (float(df.iloc[i]['high']) -float(df.iloc[i]['close']))/float(df.iloc[i]['close'])*100
    df.at[i, 'pct_chg'] = (float(df.iloc[i]['close']) - float(df.iloc[i]['high'])) / float(df.iloc[i]['high']) * 100

stocks_list = sorted(list(set(df['stock'])))


for stock in stocks_list:
    stock_df = df[df['stock']==stock]
    dates = stock_df['date']
    np.save("App/dates.npy", dates)
    stock_df = stock_df[['date','open','low','high','h_o','pct_chg','volume','close']]
    #TRAINING OF THE MODELS

    training_data = 12
    testing_data = 13
    train, test = stock_df.iloc[0:training_data], stock_df.iloc[training_data:len(stock_df)]
    
    for predicted_parameter in ['low','high']:
        X_train = train[['open','close','h_o','pct_chg','volume']]
        y_train = train[[predicted_parameter]]
        X_test = test[['open','close','h_o','pct_chg','volume']]
        y_test = test[[predicted_parameter]]
        from sklearn import linear_model
        clf = linear_model.LinearRegression().fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        a = []
        b = []
        y_test_list = y_test.values
        a = y_test_list.tolist()
        b = y_pred.tolist()
        aa = []
        for i in range(len(a)):
            aa.append(a[i][0])
        bb = []
        for i in range(len(b)):
            bb.append(b[i][0])
        line1 = plt.plot(dates[training_data:len(stock_df)], aa, 'green')
        line2 = plt.plot(dates[training_data:len(stock_df)], bb, 'red')
        #plt.legend(['Actual','Predicted'])
        #plt.show()
        filename = "App/Models/" + stock +"-"+ predicted_parameter +".sav"
        joblib.dump(clf, filename)
        #MM/DD/YYYY FROM Q1-Q2 2011