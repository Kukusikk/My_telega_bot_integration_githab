
import github, os, pdb
from dotenv import load_dotenv

load_dotenv()


def check_repo(api_token, repo):
    try:
        g = github.Github(api_token)
        # pdb.set_trace()
        repo = g.get_repo(repo)
        return repo
    except:
        return 'bad'

def check_api_token(api_token):
    try:
        g = github.Github(api_token)
        u=g.get_user()
        u.login
    except:
        return 'bad'

def create_webhok_githab(info):
    api_token = info['api_token']
    g = github.Github(api_token)
    url=f"{os.environ.get('HOST_SERVER')}/from_git_to_telega"  # хост меняется при развороте
    conf={'url': url, "content_type": "json"}

    try:
        for r in info['repo']:
            # pdb.set_trace()
            if len(r)<3:
                repo = g.get_repo(r[0])
                # pdb.set_trace()
                hok=repo.create_hook("web", conf, ['push', 'pull_request', 'create'], True)
                print(hok)
                # pdb.set_trace()
                r.append(True)
    except github.GithubException as e:
        print(str(e))
        return ['bad', "Hook already exists on this repository"]
    except Exception as e:
        print(str(e))
        return ['bad']


