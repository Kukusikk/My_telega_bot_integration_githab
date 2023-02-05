1) Команды для работы

активация среды
source my_venv/bin/activate

дезактивация
deactivate

выгрузка в файл
pip freeze > requirements.txt

загрузка из файла
pip install -r requirements.txt

2) Развертывание приложения:

- создадим приватный токен доступа в гитхабе. Запишем его в .env в значение TOKEN

- Создадим туннель к localhost с помощью ngrok. Т.к. я использую 5000 порт при запуске приложения, то прокидываю его. Полученный url прокидываю в переменную HOST_SERVER в файле .env
ngrok http  5000 - без пароля

- Создадите виртуальное окружение и установите все зависимости

- Запустим наш сервис
flask --app  endpoints.py run --host=0.0.0.0

 - Для того, чтобы Telegram пересылал сообщения на наш сервер, нужно сообщить ему адрес
$ curl --location --request POST 'https://api.telegram.org/bot{Тут токен, что вы получили при создании бота}/setWebhook' \
--header 'Content-Type: application/json' \
--data-raw '{
    "url": "Тут url, что отдал нам ngok, должен быть https"
}'
