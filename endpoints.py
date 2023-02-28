from flask import Flask, request
import pdb
import telega_logic
import requests

app = Flask(__name__)


# делаем вместо курла
curl_url = f"https://api.telegram.org/bot{os.environ.get('TOKEN')}/setWebhook"
r = requests.post(curl_url, data = {'url': os.environ.get('HOST_SERVER')})  


# ендпоинты для гитхаба
@app.route("/from_git_to_telega", methods=["GET", "POST"])
def from_git_to_telega():
    text = 'Произошло что то другое'
    if request.headers['X-Github-Event'] == 'ping':
        return {"ok": True}
    elif request.headers['X-Github-Event'] == 'push':
        text = f"Для репозитория {request.json['repository']['name']}\n был произведен пуш коммитов"
    elif request.headers['X-Github-Event'] == 'create':
        text = f"Для репозитория {request.json['repository']['name']}\n создана новая ветка"
    elif request.headers['X-Github-Event'] == 'pull_request' and request.json['repository'] == 'open':
        text = f"Для репозитория {request.json['repository']['name']}\n был открыт пулреквест"
    elif request.headers['X-Github-Event'] == 'pull_request'and request.json['repository'] != 'open':
        text = f"Для репозитория {request.json['repository']['name']}\n была произведен работа с пулреквестом"
 
    chat_ids = telega_logic.chat_ids(request.json['repository'])

    for i in set(chat_ids):
        telega_logic.send_message(i, text)
    print('from_git_to_telega')
    return {"ok": True}

# ендпоинты для телеги
@app.route("/", methods=["POST"])
def root_url():
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

    if telega_logic.params(request)[0] == "/add_project":
        telega_logic.add_project(request)
    elif telega_logic.params(request)[0] == "/my_info":
        telega_logic.my_info(request)
    elif telega_logic.params(request)[0] == "/set_api_token":
        telega_logic.set_api_token(request)
    elif telega_logic.params(request)[0] == "/set_repo":
        telega_logic.set_repo(request)
    return {"ok": True}



