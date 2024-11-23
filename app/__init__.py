from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError
import json
import os

def send_request(url, method='GET', header={}, data={}, save=False):
    if 'json' in str(header):
        data=json.dumps(data).encode()
    elif method == 'POST':
        data=urlencode(data).encode()
    elif method == 'GET' and data != {}:
        url=url+'?'+urlencode(data)

    match method:
        case 'GET':
            httprequest=Request(url)
        case 'POST':
            httprequest=Request(url, data, header, method='POST')
        case _:
            raise NotImplemented('Method still not implement.')
    if not save:
        return httprequest
    try:
        with urlopen(httprequest) as request:
            with open('data.json', 'wb') as file:
                file.write(request.read())
    except HTTPError as e: 
        raise ValueError(f'{str(e)} error arise')
def manage_data():
    push_ls, create_ls, pull_ls, fork_ls, delete_ls=[], [], \
    [], [], []
    with open('data.json', 'r') as file:
        data=json.load(file)
    if data == []:
        raise NameError('\n >We couldn\'t find any data of this user') 
    for item in data:
        match item['type']:
            case "PushEvent":
                push_ls.append(item['repo']['name'])
            case "CreateEvent":
                create_ls.append(item['repo']['name'])
            case "PullRequestEvent":
                pull_ls.append(item['repo']['name'])
            case "ForkEvent":
                fork_ls.append(item['repo']['name'])
            case "DeleteEvent":
                delete_ls.append(item['repo']['name'])
    pushs={}
    for rep in push_ls:
        if rep not in list(pushs.keys()):
            pushs[rep]=0
        else:
            pushs[rep]+=1
    return {
        'push': pushs,
        'create': create_ls,
        'pull': pull_ls,
        'fork': fork_ls,
        'delete': delete_ls
    }

def get_git_activity(url):
    send_request(url, save=True)
    data=manage_data()
    #push detail show this part
    push_dict=data['push']
    for key in list(push_dict.keys()):
        if push_dict[key] !=0:
            print(f'\n - Pushed {push_dict[key]} commits to {key}')
    #push part end
    #create part start 
    create=data['create']
    for item in create:
        print(f'\n - Started {item} repository.')
    #create end
    #delete part start 
    for item in data['delete']:
        print(f'\n - {item} repository deleted.')
    #delete part end
    #pull part start
    pull=data['pull']
    for item in pull:
        print(f'\n - A pull request to {item}')
    #pull part end
    for item in data['fork']:
        print(f'\n - A fork request at {item}')
    #pull part end

    os.remove('data.json')  #remove data.json file
    