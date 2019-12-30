import json
import requests
host = "https://2019-a15.iterator-traits.com/api"
# host = 'http://127.0.0.1:8000'


s = requests.session()

r = s.post('{}/auth/weblogin'.format(host), data={
    'username': 'admin',
    'password': 'admin'
})

f = open('project.json', 'r')
projects = json.load(f)
# cover = open('media/cover.jpg', 'r')

for project in projects:
    # project['cover'] = open("media/cover.jpg", "rb")
    r = s.post('{}/project/detail'.format(host), data=project, files=[('cover', open("media/cover.jpg", "rb"))])
    print(r.content)
