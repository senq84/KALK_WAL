from sqlite3 import Row
from flask import Flask, render_template, request
import requests
import json
import csv

app = Flask(__name__)

def get_rates():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    data = data[0]['rates']

    with open('rates.csv', 'w', encoding='UTF-8', newline='') as file:
        fieldnames = ['currency', 'code', 'bid', 'ask']
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(data)
get_rates()
amount = 0

@app.route('/', methods=['GET', 'POST'])
def home():
    
    if request.method == 'POST':
        try:
            amount = request.form['amount']
            amount = float(amount)
            from_c = request.form['from_c']
            
            response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
            data = response.json()
            data = data[0]['rates']

            row = requests.get(data, Row)

            currency = row['rates']['currency']
            code = row['rates']['code']
            rate = row['rates']['bid'] 
            rate = float(rate)
        
            result = rate * amount

            return render_template('index.html', amount=amount, response=response, 
                                   currency=currency, from_c=from_c, code=code, 
                                   rate=rate, result=round(result, 2))
        
        except Exception:
            return '<h1>Bad Request :{}</h1>'
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)



#powinna być funkcja - żeby działało w momencie obliczeń, a nie uruchomienia pojedyńczego, 
