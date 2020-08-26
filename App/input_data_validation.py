from datetime import date
from luhn import verify
import datetime

def check_credit_card_number(credit_card_number):
    return verify(credit_card_number)

def check_expiration_date(selected_date):
    today = datetime.datetime.now().date()
    d = date(int(selected_date[:4]), int(selected_date[5:7]), int(selected_date[8:]))
    return today<d

def check_security_code(code):
    if len(code)!=3:
        return False
    digits = set(['0','1','2','3','4','5','6','7','8','9'])
    for digit in code:
        if digit not in digits:
            return False
    return True

def check_positive_amount(number):
    return float(number)>0.0