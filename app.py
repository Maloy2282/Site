from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '8632946316:AAE9SWiG3RAoWOKEZiCVja6GpowsA9olW-g')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '5055425004')

@app.route('/')
def index():
    return render_template('work.html')

@app.route('/next-page')
def next_page():
    return render_template('index.html')

@app.route('/send_to_telegram', methods=['POST'])
def send_to_telegram():
    name = request.form.get('name', 'Не указано')
    tg = request.form.get('Tg', 'Не указан')
    comment = request.form.get('comment', 'Не указано')
    gender = request.form.get('Gender', 'Не указан')

    message = (
        f"<b>Новая заявка!</b>\n\n"
        f"<b>Имя:</b> {name}\n"
        f"<b>Telegram:</b> {tg}\n"
        f"<b>Нужен сайт:</b> {comment}\n"
        f"<b>Пол:</b> {gender}"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }

    try:
        response = requests.post(url, data=payload)
        response_data = response.json() 

        if response.status_code == 200 and response_data.get('ok'):
            return '''
            <h3 style="color: green;"> Данные успешно отправлены в Telegram!</h3>
            <p>Спасибо за заявку!</p>
            <a href="/">Вернуться к форме</a>
            '''
        else:
            error_description = response_data.get('description', 'Неизвестная ошибка')
            return f'''
            <h3 style="color: red;"> Ошибка отправки: {response.status_code}</h3>
            <p>Описание ошибки: {error_description}</p>
            <p>Попробуйте ещё раз или свяжитесь с наобработкими напрямую.</p>
            <a href="/">Вернуться к форме</a>
            '''
    except Exception as e:
        return f'''
        <h3 style="color: red;"> Произошла ошибка: {str(e)}</h3>
        <p>Проверьте настройки бота и ID чата.</p>
        <a href="/">Вернуться к форме</a>
        '''

if __name__ == '__main__':
    app.run()