from modules.classes import *
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
threads = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hello', methods=['POST'])
def hello():
    name = request.form['name']
    user = User.get_user(name)
    if user:
        return render_template('hello.html', name=user.username, balance=user.balance)
    else:
        return "Пользователь не найден!"


@app.route('/update_balance', methods=['POST'])
def update_balance():
    data = request.json
    user_id = data.get('userId')
    city = data.get('city')

    # Получаем текущую температуру в указанном городе
    temperature = fetch_weather(city)
    if temperature is None:
        return jsonify({'message': 'Ошибка получения данных о погоде'}), 500

    # Получаем пользователя по ID
    user = User.get_user_by_id(user_id)
    if user is None:
        return jsonify({'message': 'Пользователь не найден'}), 404

    # Вычисляем новый баланс пользователя
    new_balance = user.balance + temperature
    if new_balance < 0:
        return jsonify({'message': 'Баланс не может быть отрицательным'}), 400

    # Обновляем баланс пользователя
    user.balance = new_balance
    user.update_balance()

    return jsonify({'message': f'Баланс пользователя обновлен на {temperature}',
                    "balance": int(user.balance)}), 200



if __name__ == '__main__':
    User.create_table()
    app.run(debug=True)
