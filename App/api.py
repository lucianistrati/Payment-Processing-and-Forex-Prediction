from input_data_validation import check_expiration_date,check_security_code, check_credit_card_number, check_positive_amount
from flask import request, jsonify, render_template

import pandas as pd
import numpy as np

import requests
import joblib
import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True

CHEAP_PAYMENTS_TRIED = 0
EXPENSIVE_PAYMENTS_TRIED = 0
PREMIUM_PAYMENTS_TRIED = 0

def initialize_counters():
    global CHEAP_PAYMENTS_TRIED, EXPENSIVE_PAYMENTS_TRIED,  PREMIUM_PAYMENTS_TRIED
    CHEAP_PAYMENTS_TRIED = 0
    EXPENSIVE_PAYMENTS_TRIED = 0
    PREMIUM_PAYMENTS_TRIED = 0


@app.route('/', methods=['GET'])
def home():
    initialize_counters()
    return render_template("home.html")


def check_response_code(path):
    req = requests.get(path)
    return req.status_code
    if req.status_code == 400:
        return render_template("error-page.html", text='Bad request')
    elif req.status_code == 500 or req.status_code != 200:
        return render_template("error-page.html", text='Internal server error')


@app.route('/process-payment', methods=['GET','POST'])
def ProcessPayment():
    if request.method =='POST':
        request_answer = check_response_code('http://127.0.0.1:5000')
        if request_answer == 400:
            return render_template("error-page.html", text='Bad request')
        elif request_answer == 500 or request_answer !=200:
            return render_template("error-page.html", text='Internal server error')
        dict_form = request.form
        if check_credit_card_number(dict_form['credit-card-number'])==False:
            return render_template("error-page.html", text="Invalid credit card number")
        elif check_expiration_date(dict_form['expiration-date'])==False:
            return render_template("error-page.html", text="Selected expiration date should be in the future")
        elif check_security_code(dict_form['security-code'])==False:
            return render_template("error-page.html", text="Security code should contain 3 digits")
        elif check_positive_amount(dict_form['amount'])==False:
            return render_template("error-page.html", text="Paid amount should be a positive number")
        else:
            amount = float(dict_form['amount'])
            if amount<=20.99:
                return render_template("cheap-payment-gateway.html")
            elif amount>=21.00 and amount<=499.99:
                return render_template("expensive-payment-gateway.html")
            else:
                return render_template("premium-payment-gateway.html")


@app.route('/cheap-payment-gateway', methods=['GET','POST'])
def FinishCheapPaymentGateway():
    if request.method =='POST':
        global CHEAP_PAYMENTS_TRIED, EXPENSIVE_PAYMENTS_TRIED, PREMIUM_PAYMENTS_TRIED
        request_answer = check_response_code('http://127.0.0.1:5000')
        if request_answer == 400:
            return render_template("error-page.html", text='Bad request')
        elif request_answer == 500 or request_answer != 200:
            return render_template("error-page.html", text='Internal server error')
        dict_form = request.form
        return render_template("succesful-payment.html")



@app.route('/expensive-payment-gateway', methods=['GET','POST'])
def FinishExpensivePaymentGateway():
    if request.method =='POST':
        global CHEAP_PAYMENTS_TRIED, EXPENSIVE_PAYMENTS_TRIED, PREMIUM_PAYMENTS_TRIED
        request_answer = check_response_code('http://127.0.0.1:5000')
        if EXPENSIVE_PAYMENTS_TRIED==0 and request_answer!=200:
            FinishCheapPaymentGateway()
            EXPENSIVE_PAYMENTS_TRIED+=1
        if EXPENSIVE_PAYMENTS_TRIED==1 or request_answer == 400:
            return render_template("error-page.html", text='Bad request')
        elif request_answer == 500 or request_answer != 200:
            return render_template("error-page.html", text='Internal server error')
        return render_template("succesful-payment.html")


@app.route('/premium-payment-gateway', methods=['GET','POST'])
def FinishPremiumPaymentGateway():
    if request.method =='POST':
        global CHEAP_PAYMENTS_TRIED, EXPENSIVE_PAYMENTS_TRIED, PREMIUM_PAYMENTS_TRIED
        request_answer = check_response_code('http://127.0.0.1:5000')
        if request_answer!=200:
            if PREMIUM_PAYMENTS_TRIED==3:
                return render_template("error-page.html", text="Maximum number of requests reached, please re-enter your data")
            PREMIUM_PAYMENTS_TRIED+=1
            FinishPremiumPaymentGateway()
        if request_answer == 400:
            return render_template("error-page.html", text='Bad request')
        elif request_answer == 500 or request_answer != 200:
            return render_template("error-page.html", text='Internal server error')
        return render_template("succesful-payment.html")


def check_week(prediction_date):
    dates = np.load("dates.npy",allow_pickle=True) # MM/DD/YYYY format
    pred_month = int(prediction_date[:2])
    pred_day = int(prediction_date[3:5])
    for week in dates:
        month = int(week[:1])
        if week[1] == '/' and week[3] == '/':
            day = int(week[2])
        else:
            day = int(week[2:4])
        if month==pred_month:
            if day>=pred_day:
                return week
    return None


def check_good_date(year, month,day):
    if year!=2011 or month>6:
        return False
    return True


@app.route('/estimate-price', methods=['GET','POST'])
def EstimatePrice():
    if request.method =='POST':
        request_answer = check_response_code('http://127.0.0.1:5000')
        if request_answer == 400:
            return render_template("error-page.html", text='Bad request')
        elif request_answer == 500 or request_answer != 200:
            return render_template("error-page.html", text='Internal server error')
        dict_form = request.form
        year = dict_form['prediction-date'][:4]
        month = dict_form['prediction-date'][5:7]
        day = dict_form['prediction-date'][8:]
        if check_good_date(int(year),int(month),int(day))==False:
            return render_template("error-page.html",text="Bad request")
        new_date = month+"/"+day+"/"+year
        week = check_week(new_date)
        quote = dict_form['stock-quote']
        stock_df = pd.read_csv("Models/"+quote+".csv")
        record = stock_df[stock_df['date'] == week]
        record = record[['open', 'close', 'h_o', 'pct_chg', 'volume']]
        low_pred_path = "Models/"+quote+"-low.sav"
        model = joblib.load(low_pred_path)
        low_prediction = model.predict(record)
        high_pred_path = "Models/"+quote+"-high.sav"
        model = joblib.load(high_pred_path)
        high_prediction = model.predict(record)
        mid_range_price = (low_prediction[0][0] + high_prediction[0][0])/2
        return render_template("stock-prediction.html", quote = quote, day=dict_form['prediction-date'], price = round(mid_range_price,2))

if __name__=='__main__':
    app.run()