from flask import Flask, render_template, request
import requests
from datetime import date, timedelta, datetime
from calculadora_ig import IdadeGestacional

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/<name>')
def greet(name):
    return f'Hello, {name}!'

@app.route('/guess/<name>')
def guess(name):
    # URL da API do Genderize.io
    url = f"https://api.genderize.io?name={name}"
    # Faz a requisição GET para a API
    gender_response = requests.get(url)
    gender_data = gender_response.json()
    gender = gender_data["gender"]
    return render_template("guess.html", person_name=name, gender=gender)

@app.route('/calculoig', methods=['GET', 'POST'])
def calculoig():
    if request.method == 'POST':
        # Obtém o valor do campo 'nome' do formulário
        nome = request.form['nome']
        return f'O nome informado foi: {nome}'
    else:
        return render_template('calculo_ig.html')


@app.route('/calculadora')
def calculadora():
    return render_template('calcular.html')

@app.route('/calcular', methods=['POST'])
def calcular_idade_gestacional():
    data_ultima_menstruacao = date.fromisoformat(request.form['data_ultima_menstruacao'])
    data_primeiro_ultrassom = date.fromisoformat(request.form['data_primeiro_ultrassom'])
    idade_gestacional_ultrassom = int(request.form['idade_gestacional_ultrassom_semanas'])*7+int(request.form['idade_gestacional_ultrassom_dias'])
    ig = IdadeGestacional(data_ultima_menstruacao, data_primeiro_ultrassom, idade_gestacional_ultrassom)
    metodo, idade_final, outra_ig, outro_metodo = ig.qual_ig_usar()

    return f"<h1> Utilizar IG({metodo}): {idade_final} / IG({outro_metodo}): {outra_ig} <h1>"


if __name__ == "__main__":
    app.run(debug=True)
