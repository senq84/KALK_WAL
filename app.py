from flask import Flask, render_template, request
import requests
import csv

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def home():

    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json") 
    dane = response.json()

    if request.method == 'GET':
        stawki = dane[0]['rates']
        kody_walut = [d['code'] for d in stawki]
        print(kody_walut)
        return render_template('index.html', data=kody_walut)
    
    if request.method == 'POST':
        print(dane)
        try:          
            rates = dane[0]['rates']
            tradingDay = dane[0]['tradingDate']
            
            currency_name = rates[0]['currency']
            code = rates[0]['code']

            currency = rates[0]['currency']

            amount = request.form['amount']
            amount = float(amount)
            from_c = request.form['from_c']

            result = 0 

            for currency in rates:
                if currency['code'] == from_c:
                    result = currency['bid'] * amount
                    bid = currency['bid']
                    from_c = currency['code']

            return render_template('index.html', amount=amount, currency_name=currency_name, response=response, 
                                   currency=currency, from_c=from_c, tradingDay=tradingDay, code=code, rates=rates,
                                   bid=bid, result=round(result, 2))
        
        except Exception as e:
            return '<h1>Bad Request : {}</h1>'.format(e)

if __name__ == "__main__":
    app.run(debug=True)