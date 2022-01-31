from flask import Flask, render_template, request
import requests
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

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json") 
        dane = response.json()
        stawki = dane[0]['rates']
        kody_walut = [d['code'] for d in stawki]
        print(kody_walut)
        render_template('index.html', data=kody_walut)
    else:
        return render_template('index.html')

    if request.method == 'POST':
        try:          
            response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")  
            data = response.json()

            rates = data[0]['rates']
            tradingDay = data[0]['tradingDate']
            
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

            #zobaczyć co jest wykorzystane w szablonie 
            return render_template('index.html', amount=amount, currency_name=currency_name, response=response, 
                                   currency=currency, from_c=from_c, tradingDay=tradingDay, code=code, rates=rates,
                                   bid=bid, result=round(result, 2))
        
        except Exception as e:
            return '<h1>Bad Request : {}</h1>'.format(e)
  
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)