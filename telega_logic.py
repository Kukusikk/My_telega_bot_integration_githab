import githab_logic, os
import requests, pdb

array_chats = {}

def add_project(request):
    info = array_chats.get(chat_id(request), {})

    if not info:
        return send_message(chat_id(request), "Введите ваш api_token используя /set_api_token и название репозитория используя /set_repo")

    res = githab_logic.create_webhok_githab(info)

    if not isinstance(res, list):
        return send_message(chat_id(request), "Вебхук успешно создан")

    if len(res) == 1:
        return send_message(chat_id(request), "Ваш вебхук не смог создасться")

    send_message(chat_id(request), res[1])

def my_info(request):
    info = array_chats.get(chat_id(request), {})
    send_message(chat_id(request), f"Ваши данные: {info}")

def set_api_token(request):
    api_token = params(request)[1]

    if githab_logic.check_api_token(api_token)!= 'bad':
        now_info = array_chats.get(chat_id(request), {})
        if now_info:
            now_info['api_token'] = api_token
        else:
            array_chats[chat_id(request)] = {'api_token': api_token}

        send_message(chat_id(request), "Ваш api_token успешно сохранен")
    else:
        send_message(chat_id(request), "Ваш api_token не валидный")


# вида "Kukusikk/django_project_password"
def set_repo(request):
    now_info = array_chats.get(chat_id(request), {})
    # pdb.set_trace()
    if (now_info is None) or (now_info.get('api_token', None) is None):
        return send_message(chat_id(request), "Ваш api_token пустой")

    repo_name = params(request)[1]
    repo = githab_logic.check_repo(now_info['api_token'], repo_name)

    if repo!= 'bad':
        now_repo = now_info.get('repo', [])
        now_repo.append( [repo_name, repo.id])
        now_info['repo'] = now_repo
        send_message(chat_id(request), "Ваш репозиторий успешно сохранен")
    else:
        send_message(chat_id(request), "Ваш репозиторий не валидный")


def chat_id(request):
    ms = request.json.get("message", None) or request.json.get("edited_message", None)
    return ms["chat"]["id"]

def params(request):
    ms = request.json.get("message", None) or request.json.get("edited_message", None)
    return ms['text'].split(' ')

def chat_ids(rep):
    rep_id = rep['id']
    ids = []

    for us_id in array_chats:
        flag_add = [ j for j in array_chats[us_id]['repo'] if j[1] == rep_id]

        if flag_add:
            ids.append(us_id)
    return ids

def send_message(chat_id, text):
    method = "sendMessage"
    url = f"https://api.telegram.org/bot{os.environ.get('TOKEN')}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)
