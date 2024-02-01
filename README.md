## Как запустить
* Склонировать репозиторий
* Прописать в нужное питоновское окружение pip install -r requirements.txt
* Теперь нужно создать приложение в дискорде и добавить туда бота, а также добавить бота на нужный сервер. Это хорошо расписано вот [тут](https://appmaster.io/ru/blog/bot-discord-kak-sozdat-i-dobavit-na-server)
* После этого копируем токен бота и добавляем в config.py
* Также нужно настроить бота на сервере, чтобы его могли использовать только преподаватели, для этого нужно создать роли на серере и выдать разрешения для них
* Теперь нужно подключить google sheets, как это сделать расписано [тут](https://pypi.org/project/gsheets/), и заменить путь к таблице в файле google_api.py
