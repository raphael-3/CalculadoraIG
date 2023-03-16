import os
from flask import Flask, render_template, request, send_from_directory
import requests
from datetime import date, timedelta, datetime
from calculadora_ig import IdadeGestacional

app = Flask(__name__)

app.config['uploads'] = 'uploads' # Diretório onde as imagens serão armazenadas


@app.route('/')
def main():
    return render_template('captura_imagem.html')

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

#### PEGAR IMAGEM #####

@app.route('/captura_imagem')
def capturar():
    return render_template('captura_imagem.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Salva a imagem enviada no diretório uploads
    file = request.files['imagem']
    filename = file.filename
    file.save(os.path.join(app.config['uploads'], filename))

    # Renderiza a página de exibição da imagem
    return render_template('view.html', filename=filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Retorna a imagem armazenada no diretório uploads
    return send_from_directory(app.config['uploads'], filename)

# @app.route('/upload', methods=['POST'])
# def upload():
#     file = request.files['image']
#     # Faça algo com a imagem aqui
#     return 'Imagem recebida com sucesso!'


##### CALCULADORA IG ########
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
