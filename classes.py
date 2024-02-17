import sqlite3
import requests
from random import randint


def fetch_weather(city):
    api_key = '1dca9fcb025f5918465f1f220aaf22ae'  # API ключ
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  # температура в градусах Цельсия
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if data['cod'] == 200:  # Проверяем статус код ответа
            temperature = data['main']['temp']
            return temperature
        else:
            print("Ошибка получения данных:", data['message'])
            return None
    except Exception as e:
        print("Ошибка:", e)
        return None


class User:
    def __init__(self, username, balance=0):
        self.username = username
        self.balance = balance

    @staticmethod
    def create_table():
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                balance REAL NOT NULL
            );
        ''')
        for i in range(1, 6):
            username = f"user{i}"
            balance = randint(5000, 15000)
            cursor.execute('''
                INSERT INTO users (username, balance) VALUES (?, ?);
            ''', (username, balance))
        conn.commit()
        conn.close()

    def save(self):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, balance) VALUES (?, ?)
        ''', (self.username, self.balance))
        conn.commit()
        conn.close()

    @staticmethod
    def get_user(username):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        user = cursor.fetchone()
        conn.close()
        if user:
            return User(user[1], user[2])
        return None

    def update_balance(self):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET balance=? WHERE username=?
        ''', (self.balance, self.username))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_user(username):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE username=?', (username,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_user_by_id(user_id):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id=?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        if user:
            return User(user[1], user[2])
        return None


# Пример использования класса User
if __name__ == '__main__':
    # User.create_table()
    #
    # # Создание пользователя и сохранение его в базу данных
    # user1 = User('user1', balance=10000)
    # user1.save()
    #
    # # Получение пользователя из базы данных по имени
    # user2 = User.get_user('user1')
    # print(user2.username, user2.balance)  # Выводит: user1 10000
    #
    # # Обновление баланса пользователя
    # user2.balance += 500
    # user2.update_balance()
    #
    # # Удаление пользователя из базы данных
    # User.delete_user('user1')

    # Пример использования функции fetch_weather
    city = 'Kazan'  # Задаем город, для которого хотим получить погоду
    temperature = fetch_weather(city)
    if temperature is not None:
        print(f"Текущая температура в городе {city}: {temperature} градусов Цельсия")
    else:
        print("Не удалось получить данные о погоде")
