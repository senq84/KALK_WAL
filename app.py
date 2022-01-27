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
    if request.method == 'POST':
        try:
            amount = request.form['amount']
            amount = float(amount)
            from_c = request.form['from_c']
            
            response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json") # tutaj można w nawiasie ew. zmieniać żeby pobierać z poliku .csv  
            data = response.json()
            rates = data[0]['rates']
            tradingDay = data[0]['tradingDate']
            
            result = 0 

            for currency in rates:
                if currency['code'] == from_c:
                    result = currency['bid'] * amount
                    bid = currency['bid']
                    from_c = currency['code']

            #zobaczyć co jest wykorzystane w szablonie 
            return render_template('index.html', amount=amount, response=response, 
                                   currency=currency, from_c=from_c, tradingDay=tradingDay, 
                                   bid=bid, result=round(result, 2))
        
        except Exception as e:
            return '<h1>Bad Request : {}</h1>'.format(e)
  
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
